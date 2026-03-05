CREATE DATABASE IF NOT EXISTS sr;
USE sr;

DELIMITER //
CREATE TRIGGER update_assigned
AFTER INSERT ON report FOR EACH ROW
BEGIN
    DECLARE year_part VARCHAR(4);
    DECLARE prev_year INT;
    DECLARE prev_prev_year INT;

    -- 보고서명( ex. 사업보고서(2023.06) )에서 사업연도 추출 및  전년도, 전전년도 계산
    SET year_part = CAST(SUBSTRING_INDEX(SUBSTRING_INDEX(NEW.report_nm, '(', -1), '.', 1) AS UNSIGNED);
    SET prev_year = year_part - 1;
    SET prev_prev_year = prev_year - 1;

    -- 지정감사라고 판별된 보고서
    IF NEW.is_audit_currently_assigned != '-' THEN

        INSERT IGNORE assigned (corp_code, assigned_year, assigned.description)
        VALUES (NEW.corp_code, year_part, NEW.description); -- 올해 사업연도 추가

        -- 지정감사 2년차 이상 ( 당기 감사인 = 전기 감사인 )
        IF NEW.auditor_now = NEW.auditor_prior AND NOT EXISTS (SELECT 1 FROM assigned WHERE corp_code = NEW.corp_code AND assigned_year = prev_year) THEN
            INSERT IGNORE assigned (corp_code, assigned_year, assigned.description)
            VALUES (NEW.corp_code, prev_year,  NEW.description); -- 전년도 추가
        
            -- 지정감사 3년차 ( 당기 감사인 = 전전기 감사인)
            IF NEW.auditor_now = NEW.auditor_two_years_ago AND NOT EXISTS (SELECT 1 FROM assigned WHERE corp_code = NEW.corp_code AND assigned_year = prev_prev_year) THEN
                INSERT IGNORE assigned (corp_code, assigned_year, assigned.description)
                VALUES (NEW.corp_code, prev_prev_year, NEW.description); -- 전전년도 추가
            END IF;
        END IF;
    END IF;

    -- 지정감사가 아니라고 판별된 보고서
    IF NEW.is_audit_currently_assigned = '-' THEN
        -- 실제로는 지정감사 2년차 이상인 경우 ( assigned 테이블에 이력이 있는 경우 )
        IF EXISTS(SELECT 1 FROM assigned WHERE (corp_code = NEW.corp_code AND assigned_year = prev_year) OR (corp_code = NEW.corp_code AND assigned_year = prev_prev_year)) THEN
            -- 지정감사 2년차 이상 ( 당기 감사인 = 전기 감사인 ) 재검증
            IF NEW.auditor_now = NEW.auditor_prior THEN
                INSERT IGNORE assigned (corp_code, assigned_year, assigned.description)
                VALUES (NEW.corp_code, year_part, NEW.description), (NEW.corp_code, prev_year, NEW.description); -- 올해 사업연도, 전년도 추가

                -- 지정감사 3년차 (당기 감사인  = 전전기 감사인)
                IF NEW.auditor_now = NEW.auditor_two_years_ago THEN
                    INSERT IGNORE assigned (corp_code, assigned_year, assigned.description)
                    VALUES (NEW.corp_code, prev_prev_year, NEW.description); -- 전전년도 추가
                END IF;
            END IF;
        END IF;
    END IF;
END;
//
DELIMITER ;