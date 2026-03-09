from urllib3.exceptions import InsecureRequestWarning
from bs4 import BeautifulSoup as BS
from transformers import pipeline
from tqdm.auto import tqdm
import pandas as pd
import requests
import time
import zipfile
import json
import io
import re
import os
import collections
collections.Callable = collections.abc.Callable
os.environ['TRANSFORMERS_OFFLINE']='1'
import warnings

def make_update_target(bgn_de:str, end_de:str):
    """bgn_de부터 end_de까지 공시된 보고서들을 확인하고, 각 보고서의 정보가 담긴 DataFrame을 반환

    Args:
        bgn_de : 시작일
        end_de : 종료일

    Returns:
        update_target (pd.DataFrame) : columns=['corp_code', 'corp_name', 'stock_code', 'corp_cls', 'report_nm', 'rcept_no', 'flr_nm', 'rcept_dt', 'rm']
    """
    api = 'https://opendart.fss.or.kr/api/list.json'
    params = {
        'crtfc_key': 'your_opendart_api_key',
        'bgn_de': bgn_de,
        'end_de': end_de,
        'pblntf_ty': 'A',
        'page_count': "100",
    }

    update_target = pd.DataFrame(columns=['corp_code', 'corp_name', 'stock_code', 'corp_cls', 'report_nm', 'rcept_no', 'flr_nm', 'rcept_dt', 'rm'])

    res = requests.get(api, params=params)
    result = json.loads(res.text)
    tot_page = result['total_page']

    for i in tqdm(range(tot_page)):
        params['page_no'] = i + 1
        res = requests.get(api, params=params)
        result = json.loads(res.text)

        if not update_target.empty:
            update_target = pd.concat([update_target, pd.DataFrame(result['list'])], ignore_index=True)
        else:
            update_target = pd.DataFrame(result['list'])

        time.sleep(0.02)
        
    return update_target

def get_xml(rcept_no:str, api_key:str):
    """Dart의 OpenAPI를 이용하여 입력받은 rcept_no에 해당하는 보고서를 저장

    Args:
        rcept_no : api를 통해 다운받을 보고서 번호
        api_key : Dart OpenAPI key

    Returns:
        xml_content, res.content (tuple) : 원문, 원문 byte로 변환
    """
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    api = 'https://opendart.fss.or.kr/api/document.xml'
    res = requests.get(api, 
                       params={
                           'crtfc_key': api_key, 
                           'rcept_no': rcept_no
                           }, verify=False)

    zip_file = io.BytesIO(res.content)

    # Zip 파일 읽기
    with zipfile.ZipFile(zip_file, "r") as zip_file:
        for file_name in zip_file.namelist():
            if "_" not in file_name:
                try:
                    with zip_file.open(file_name) as file:
                        xml_content = file.read().decode('cp949')
                except:
                    try:
                        with zip_file.open(file_name) as file:
                            xml_content = file.read().decode('utf-8')
                    except:
                        with zip_file.open(file_name) as file:
                            xml_content = file.read().decode('ANSI')      
                          
                xml_content = xml_content.replace('\x80', '')
    return xml_content, res.content


def extract_information(rcept_no:str, xml_df: pd.DataFrame, pipe: pipeline):
    """xml 원문을 한 번에 처리해주는 함수
    1. xml 원본 bs4로 필요 부분(감사인의 감사의견 페이지) 추출
    2. 감사인이 column에 들어간 표들 추출
    3. 추출된 표들로부터 필요 정보(각 기별 감사인 추출, 보수 및 시간 추출)
    4. 객체인식 모델을 이용하여 지정감사 여부 추출

    Args:
        rcept_no : 보고서번호
        xml_df : 원문이 저장된 DataFrame
        pipe : 사용되는 객체인식 모델 파이프라인

    Returns:
        dictionary: 최종적으로 DB에 저장될 정보를 dictionary형식으로 반환
    """
    # 1. xml 원본 bs4로 필요 부분(감사인의 감사의견 페이지) 추출
    warnings.filterwarnings("ignore", category=UserWarning, message=".*XMLParsedAsHTMLWarning.*")
    dsd_xml = xml_df.loc[xml_df['rcept_no'] == rcept_no, 'xml_content'].values[0]
    if dsd_xml != None:
        dsd_xml = dsd_xml.replace('&cr;', '')
    else:
        return {'is_changed': "추출불가"}
    dsd_xml = re.sub('\n', '', dsd_xml)
    dsd_xml = re.sub(r'<TE(.*?)>(.*?)</TE>', r'<TD\1>\2</TD>', dsd_xml)
    dsd_xml = re.sub(r'<TU(.*?)>(.*?)</TU>', r'<TD\1>\2</TD>', dsd_xml)

    soup = BS(dsd_xml, 'lxml')

    title_tag = soup.find('title', {'atoc': 'Y', 'aassocnote': 'D-0-5-0-0'})
    if title_tag and "감사인" in title_tag.text.strip():
        section1_pattern = re.compile(r"<SECTION-1((?!<SECTION-1)[\S\s\n])*?(D-0-5-0-0)[\S\s\n]*?</SECTION-1>") 
    else:
        section1_pattern = re.compile(r"<SECTION-1((?!<SECTION-1)[\S\s\n])*?(D-0-4-\d-\d)[\S\s\n]*?</SECTION-1>")
    section1_section = section1_pattern.search(dsd_xml)
    
    section1_section = section1_section.group()
    
    target_page = BS(section1_section, 'lxml')
  
    try:
        original_tables_xml = target_page.find_all("table")
        df = pd.read_html(target_page.prettify())

    except:
        return {'is_changed': "추출불가"}
    
    # 2. 감사인이 column에 들어간 표 추출
    auditor_in_heads = get_auditor_in_heads(df)

    if not auditor_in_heads:
        return {'is_changed': "추출불가"}
    
    # 3. 위에서 추출된 표로부터 필요정보 추출
    # 감사인의 변동여부
    auditor_changed_result = extract_auditor_change_from_table(auditor_in_heads)

    # 보수 및 시간
    earning_time_result = extract_contents_earning_worktime_from_table(auditor_in_heads, section1_section)

    # 4. 객체인식모델을 이용하여 지정감사 여부 추출
    specified_audit_result = identify_specified_audit(section1_section, pipe, auditor_changed_result['auditor_now'])

    tables_xml = ""
    for table in original_tables_xml:
        tables_xml += str(table) + "<br>"

    return add_dicts(auditor_changed_result, earning_time_result, {"auditor_in_heads" : tables_xml}, {'xml_content':xml_df.loc[xml_df['rcept_no'] == rcept_no, 'xml_content_byte'].values[0]}, specified_audit_result)

# dictionary 형식으로 반환을 도와주는 함수
def add_dicts(*args):
    result = {}
    for d in args:
        result.update(d)
    return result

# text에 target_list에 해당하는 단어가 하나라도 있는지 확인하는 함수
def check_word_presence(text, target_list):
    for item in target_list:
        if item in text:
            return True
    return False

# entity_recognition 리스트에  auditor_now가 있는지 확인하는 함수
def check_auditor_presence(entity_recognition, auditor_now):
    for i in entity_recognition:
        if i['word'] == auditor_now:
            return True
    return False

def identify_specified_audit(section1_section: str, pipe, auditor_now: str):
    """주어진 텍스트에서 지정감사 여부를 식별하는 함수.
    1. "회계감사인의 변경" 부분 추출
    2. '11조', '증권선물위원회', '금융감독원', '주기적 지정', '상장' 中 하나 이상이 포함되었는지 확인
    3. 포함된 경우 NER(Named Entity Recognition) 모델을 통해 조직(회계법인) 인식
    4. 추가로 "회계감사인의 변경" 부분에 해당 사업연도의 감사인이 포함된 경우, 지정감사로 판단
    
    Args:
        section1_section : 감사 정보를 포함한 텍스트.
        pipe: Hugging Face Transformers 언어모델의 pipeline 객체.
        auditor_now: 현재 감사인의 정보.

    Returns:
        dict: 식별된 감사 유형과 해당 정보가 담긴 딕셔너리.
    """
    #1. "회계감사인의 변경" 부분 추출
    section1_section = re.sub(r'<[^>]*>', '', section1_section)
    pattern = re.compile(r"(?<![20\d\d.])[\d\w]\.( ?)회계감사인의 변경(.*?)(?<![20\d\d.])[\d\w]\.")
    match = pattern.search(section1_section)
    
    if match:
        result = []
        extracted_text = match.group()
        # 2. '11조', '증권선물위원회', '금융감독원', '주기적 지정', '상장' 中 하나 이상이 포함되었는지 확인
        target_list = ['11조', '증권선물위원회', '금융감독원', '주기적 지정', '상장']
        presence = check_word_presence(extracted_text, target_list)
        if presence:
        # 3. 포함된 경우 NER(Named Entity Recognition) 모델을 통해 조직(회계법인) 인식
            data = pipe(extracted_text)
            if data:
                entity_recognition = []
                for i in range(len(data) - 1):                    
                    if data[i]['word'] in ["▁", "주", "▁(", "("] or data[i]['entity'] != 'I-ORG':
                        continue
                    if data[i]['end'] == data[i + 1]['start']:
                        combined_word   = data[i]['word'] + data[i + 1]['word']
                        combined_entity = data[i]['entity']
                        data[i + 1]['word'] = combined_word.replace("▁", "").replace(")", "")
                        data[i + 1]['entity'] = combined_entity
                    else:
                        data[i]['word'] = data[i]['word'].replace("▁", "").replace(")", "")
                        entity_recognition.append(data[i])

                if data[-1]['word'] not in ["▁", "주", "▁(", "("] and data[-1]['entity'] == 'I-ORG':
                    data[-1]['word'] = data[-1]['word'].replace("▁", "").replace(")", "")
                    entity_recognition.append(data[-1])

        # 4. 추가로 "회계감사인의 변경" 부분에 해당 사업연도의 감사인이 포함된 경우, 지정감사로 판단
                if  entity_recognition and check_auditor_presence(entity_recognition, auditor_now): # 지정감사
                    result = ["지정감사", extracted_text]

        if not result:
            result = [None, extracted_text]
            
        return dict(zip(['is_audit_currently_assigned', 'description'], result))

    else:
        result = [None, None]
        return dict(zip(['is_audit_currently_assigned', 'description'], result))
    
    
def get_auditor_in_heads(df: list(pd.DataFrame)): 
    """모든 표 중, 감사인 정보가 담긴 데이터프레임 리스트를 추출하는 함수.
    헤더가 없는 표의 경우, 첫 두 행을 확인하여 헤더 생성.

    Args:
        df : 감사인 정보가 포함된 데이터프레임 리스트.

    Returns:
        auditor_in_heads (List[pd.DataFrame]) : 감사인 정보가 담긴 데이터프레임 리스트.
    """
    auditor_in_heads = []

    for target in df:
        # 표에 내용은 없고 "-"로만 채워진 경우 넘기기
        none_count=0
        for lst in target.values:
            lst = list(lst)
            length = len(lst)
            if lst.count('-')<=length-2:
                break
            none_count+=lst.count('-')

        if none_count>=(length-1)*len(target):
            continue
        
        # theader가 없어서 DataFrame이 column이 없는 경우, tbody의 첫번째 줄을 header로 만들기
        if list(target.columns)[0] == 0 and len(list(target.columns))!=1:
            target.columns = target.iloc[0].copy()
            target = target[1:].reset_index(drop=True)

        # 감사인이 column에 있다면 결과에 추가
        if "감사인" in str(target.columns) and len(list(target.columns))!=1:
            auditor_in_heads.append(target)
            continue
        
        # row방향이 아닌 column방향으로만 되어있는 경우도 추가
        if re.search(r"(제\s*)?\d+\s*(?:기|년)",str(target.columns)) and len(target.columns)>1 and len(target) == 1:
            auditor_in_heads.append(target)
            continue

    return auditor_in_heads

def remove_spaces_and_special_characters(input_string: str):
    """문자열에서 공백과 특수문자를 제거하는 함수.

    Args:
        input_string : 공백과 특수문자를 제거하고자 하는 문자열.

    Returns:
        str: 공백과 특수문자가 제거된 문자열.
    """
    if isinstance(input_string):
        input_string = re.sub(r'[^가-힣a-zA-Z]', '', input_string)
        return input_string 
    return ''

def extract_auditor_change_from_table(auditor_in_heads: list(pd.DataFrame)): 
    """감사인 변경여부 정보를 추출하는 함수.
    1. 첫 번째 표에 접근 (일부 예외case 처리)
    2. 3년간의 감사인 추출
    3. 해당 사업연도와 전년도 감사인 비교

    Args:
        auditor_in_heads : 감사인 정보가 담긴 데이터프레임 리스트.

    Returns:
        dict: 추출한 감사인 변경여부 정보가 담긴 딕셔너리.
    """
    for i in range(len(auditor_in_heads)):
        # 감사인이 하나의 row에 적힌 경우 transpose
        if re.search(r"(제\s*)?\d+\s*(?:기|년)",str(auditor_in_heads[i].columns)):
            cnt = 0
            for num in re.findall(r'\d+',str(auditor_in_heads[i].columns)):
                num = int(num)
                if cnt:
                    if num == 1+prev_num:
                        reverse = True
                    else:
                        reverse = False
                    break
                prev_num = num
                cnt+=1
            
            target = pd.DataFrame(columns=["년도/기","감사인"])
            year = list(auditor_in_heads[i].columns)
            auditor = list(auditor_in_heads[i].iloc[0])

            if reverse:
                year.reverse()
                auditor.reverse()

            target["년도/기"] = year
            target["감사인"] = auditor
            break

        # '감사인'이라는 글귀가 column에 포함된 표들중 row의 길이가 1이 아니고 column의 길이가 1이 아닌 가장 첫 번째 table
        elif len(auditor_in_heads[i]) != 1 and len(list(auditor_in_heads[i].columns))!=1:
            target = auditor_in_heads[i]
            break
        
        # 해당 사업보고서가 제1기에 해당하며 하나의 감사인의 정보가 row가 1인 table에 적힌 경우
        elif len(auditor_in_heads[i]) == 1 and len(list(auditor_in_heads[i].columns))!=1 and "감사의견" in str(auditor_in_heads[i].columns):
            target = auditor_in_heads[i]
            break
    try:
        # 감사인/회계감사인 등 다양한 column으로 표시되고 위치 또한 정해진 틀이 없기 때문에 column의 index로 접근
        # while True:
        
        for idx in range(len(list(target.columns))):
            col = list(target.columns)[i]
            if "감사인" in col:
                break

    # 가장 윗줄부터 채워넣지 않고 두번째 줄부터 채워넣은 경우 해당 줄을 지우는 과정
        while target.iloc[0][idx] == "-" or "해당사항없음" in remove_spaces_and_special_characters(target.iloc[0][idx]):
            target = target.iloc[1:].reset_index(drop=True)

        auditor_cur = remove_spaces_and_special_characters(target.iloc[:, idx][0])
        
        # 사업보고서가 작성된 분기가 제1기이거나 신규인 회계법인
        if len(target)==1 or target.iloc[:, idx][1] == '-':
            result = ['신규', auditor_cur, None, None]
        else:
            auditor_pre = remove_spaces_and_special_characters(target.iloc[:, idx][1])
            if auditor_cur == auditor_pre:
                auditor_changed = '변경안됨'
            else:
                auditor_changed = '변경됨'
            
            if len(target) >= 3 and target.iloc[:, idx][2] != '-':
                result = [auditor_changed, auditor_cur, auditor_pre, str(remove_spaces_and_special_characters(target.iloc[:, idx][2]))]
            else:
                result = [auditor_changed, auditor_cur, auditor_pre, None]            
                
    except:
        result = ['추출불가_감사인 변경 추출에서 오류', None, None, None]

    return dict(zip(['is_changed', 'auditor_now', 'auditor_prior', 'auditor_two_years_ago'], result))

def find_all_occurrences(string: str, substring: str):
    """문자열 내에서 substring의 모든 등장 위치를 찾아 리스트로 반환하는 함수

    Args:
        string : 검색 대상 문자열
        substring : 찾고자 하는 문자열

    Returns:
        positions (list) : 찾고자 하는 문자열의 등장 위치 index가 담긴 list
    """
    positions = []
    index = 0
    while True:
        index = string.find(substring, index)
        if index == -1:
            break
        positions.append(index)
        index += 1
    return positions

def extract_contents_earning_worktime_from_table(auditor_in_heads: list(pd.DataFrame), section1_section: str):
    """감사인의 보수와 시간 정보를 추출하는 함수.
    1. "보수", "시간", "감사인" 이 헤더에 존재하는 표 선택
    2. 선택한 표 직전 표의 끝 ~ 선택한 표의 끝 부분에서 단위 추출
    3. 감사인, 감사 내용, 보수 및 시간(실제, 계약) 추출

    Args:
        auditor_in_heads : 감사인 정보가 담긴 데이터프레임 리스트.
        section1_section : "V. 회계감사인의 감사의견 등"의 내용.

    Returns:
        dict: 추출한 보수와 시간 정보가 담긴 딕셔너리.
    """
    i = 0
    while True:
        if len(auditor_in_heads) <= i:
            result = ['추출불가_보수 / 시간 추출에서 오류', None, None, None, None, None, None, None, None]
            return dict(zip(['auditor_payed', 'audit_contents', 'earnings_actual', 'worktime_actual', 'earnings_contract', 'worktime_contract', 'unit', 'earnings_actual_unit', 'earnings_contract_unit'], result))

        target: pd.DataFrame = auditor_in_heads[i]

        if target.empty:
            i+=1
            continue
        
        target_str = str(target.columns)
        if '보수' in target_str and '시간' in target_str and '감사인' in target_str:
            break
        elif '보수' in str(target.iloc[0]) and '시간' in str(target.iloc[0]) and '감사인' in str(target.iloc[0]):
            target.columns = target.iloc[0]
            target = target[1:].reset_index(drop=True)
            target.columns.name=None
            break
        i += 1
    try:
        cnt = 0
        idx_dict = {"감사인":0,"내용":0,"보수1":0,"보수2":0,"시간1":0,"시간2":0}
        column_list = list(target.columns)

        for col in column_list:
            if "보수" in str(col):
                if not idx_dict["보수1"]:
                    idx_dict['보수1']=cnt
                else:
                    idx_dict['보수2']=cnt
            elif "시간" in str(col):
                if not idx_dict["시간1"]:
                    idx_dict['시간1']=cnt
                else:
                    idx_dict['시간2']=cnt
            elif "감사인" in str(col):
                idx_dict['감사인']=cnt
            elif "내용" in str(col).replace(' ',''):
                idx_dict['내용'] = cnt
            cnt+=1

        while list(target.iloc[0])[idx_dict['보수1']] == '-' and list(target.iloc[0])[idx_dict['보수2']]=='-' and list(target.iloc[0])[idx_dict['감사인']]=='-':
            target = target.iloc[1:].reset_index(drop=True)
        
        # 가격 단위 추출
        if i == 0:
            match = re.search(r'\(단위\s*:\s*(.*?)\)', section1_section[:find_all_occurrences(section1_section, '</TABLE>')[i]])
        else:
            match = re.search(r'\(단위\s*:\s*(.*?)\)', section1_section[find_all_occurrences(section1_section, '</TABLE>')[i-1]:find_all_occurrences(section1_section, '</TABLE>')[i]]) # 직전 표 끝 ~ 해당 표 끝

        if match:
            unit = match.group(1)
            unit = unit[:20]
        else:
            unit = None     

        result = [
            target.iloc[0][column_list[idx_dict['감사인']]],

            target.iloc[0][column_list[idx_dict['내용']]],

            list(target.ilocㅅ[0])[idx_dict['보수1']] if not idx_dict['보수2'] 
            else list(target.iloc[0])[idx_dict['보수2']],

            list(target.iloc[0])[idx_dict['시간1']] if not idx_dict['보수2']
            else list(target.iloc[0])[idx_dict['시간2']],

            None if not idx_dict['보수2']
            else list(target.iloc[0])[idx_dict['보수1']],

            None if not idx_dict['보수2']
            else list(target.iloc[0])[idx_dict['시간1']],

            unit,

            extract_number_from_string(str(list(target.iloc[0])[idx_dict['보수1']]),unit) if not idx_dict['보수2']
            else extract_number_from_string(str(list(target.iloc[0])[idx_dict['보수2']]),unit),

            None if not idx_dict['보수2']
            else extract_number_from_string(str(list(target.iloc[0])[idx_dict['보수1']]),unit),
        ]

    except:
        result = ['추출불가_보수 / 시간 추출에서 오류', None, None, None, None, None, None, None, None]
    return dict(zip(['auditor_payed', 'audit_contents', 'earnings_actual', 'worktime_actual', 'earnings_contract', 'worktime_contract', 'unit', 'earnings_actual_unit', 'earnings_contract_unit'], result))

def remove_bracket_and_sum_numbers(input_string: str):
    """괄호 및 특수문자를 제거하고 숫자들을 추출하여 합산하는 함수.

    Args:
        input_string : 숫자를 추출하고자 하는 문자열.

    Returns:
        tot_num (int) : 추출한 숫자들을 합산한 결과.
    """
    tot_num = 0
    input_string_splited = input_string.split(" ")
    for number in input_string_splited:
        if isinstance(number, str):
            number = re.sub(r'\([^)]*\)', '', number)
            number = re.sub(r'[^\d,.]', '', number)
            tot_num += parse_numbers_with_commas(number)
    return tot_num

def parse_numbers_with_commas(text: str):
    """쉼표가 포함된 문자열에서 숫자를 추출하고 합산하는 함수. 예를 들어 "1,000,000"이 주어지면 1000000을 반환.
    여러 줄이 한 셀에 들어있는 경우 역시 처리. 예를 들어 "10,00020,000"이 주어지면 30000을 반환.

    Args:
        text : 숫자를 추출하고자 하는 문자열.

    Returns:
        int: 추출한 숫자들을 합산한 결과.
    """
    merged_numbers = []
    number_buffer = ""
    
    after_comma = False
    tmp_buffer = ""
    for i in range(len(text)):
        char = text[i]
        if after_comma and char != ",":
            number_buffer += char
            tmp_buffer += char
            if not len(tmp_buffer) % 3:
                if i != len(text)-1 and text[i+1] == ",":
                    continue
                else:
                    merged_numbers.append(int(number_buffer))
                number_buffer = ""
                tmp_buffer = ""
                after_comma = False
        elif char == ",":
            after_comma = True
        else:
            number_buffer += char

    if number_buffer:
        merged_numbers.append(eval(number_buffer))    
    return sum(merged_numbers)

def extract_number_from_string(input_string: str, unit: str):
    """문자열에서 숫자를 추출하고 단위를 적용하여 숫자로 변환하는 함수.
    예를 들어 "1천만원"이 주어지면 10000000을 반환. 단위가 제공되지 않은 경우에는 추출한 숫자를 그대로 반환.

    Args:
        input_string : 숫자를 추출하고자 하는 문자열.
        unit : 단위로 사용될 문자열.

    Returns:
        추출한 숫자에 단위를 곱한 결과. 이상치의 경우 "-" 반환.
    """
    if unit is not None:
        input_string = input_string+unit

    unit_dict = {"억":100000000,"천만": 10000000, "백오십만": 1500000, "백만":1000000, "십만":100000, "10만":100000, "만":10000,"천":1000, "RMB" : 178, "CNY" :178, "USD" : 1280 ,"백":1000000}    
    actual_unit = 1

    remaining_string = input_string
    for key in unit_dict.keys():
        if key in remaining_string:
            actual_unit*=unit_dict[key]
            remaining_string = remaining_string.replace(key, "")
    
    value = remove_bracket_and_sum_numbers(input_string)

    if value and value * actual_unit < 100000000000:
        return value * actual_unit
    else:
        return "-"
    
def write_result_csv(df: pd.DataFrame, xml_df: pd.DataFrame):
    """어제 공시된 보고서 목록이 담긴 df와 각 보고서 원문이 담긴 xml_df을 기반으로 보고서 정보를 추출하고 DB에 적재할 최종 DataFrame을 반환하는 함수.

    Args:
        df : 보고서 정보가 담긴 DataFrame.
        xml_df : XML 파일에서 추출한 정보가 담긴 DataFrame.

    Returns:
        result (pd.DataFrame) : 보고서 정보와 추출한 결과가 추가된 DataFrame.
    """
    pipe = pipeline("token-classification", model="xlm-roberta-large-finetuned-conll03-english")

    tmp_df_for_append = []
    for i in tqdm(range(len(df))):
        try:
            flag = True
            rcept_no = df['rcept_no'][i]
            report_nm = df['report_nm'][i]
            if check_is_not_target(report_nm):
                information = {'is_changed': "추출 대상 보고서 아님"}
            else:
                flag = False
                information = extract_information(rcept_no, xml_df, pipe)
        except Exception as e:
            print("에러 : ", e)
            if flag:
                information = {'is_changed': "추출불가_다운 오류"} #014에러 / connection
            else:
                information = {'is_changed': "추출불가_추출 오류"}
        tmp_df_for_append.append(information)
    
    answer_df = pd.DataFrame(tmp_df_for_append)
    answer_df = fill_missing_columns(answer_df, columns_list=[
                            'is_changed', 'auditor_now', 'auditor_prior', 'auditor_two_years_ago', 'auditor_payed', 
                            'audit_contents', 'earnings_actual', 'worktime_actual', 
                            'earnings_contract', 'worktime_contract', 'unit', 
                            'earnings_actual_unit', 'earnings_contract_unit', 'auditor_in_heads', 'xml_content', 'is_audit_currently_assigned', 'description'], 
                            default_value=None)
    
    result = pd.concat([df, answer_df], axis=1)
    result.fillna('-', inplace=True)
    for i in ['earnings_actual_unit', 'earnings_contract_unit']:
      result.loc[result[i] == '-', i] = 0 
    result['xml_content'].replace('-', None, inplace=True)
    return result

def check_is_not_target(input_string: str):
    """주어진 문자열에 특정 패턴이 존재하는지 확인하는 함수.

    Args:
        input_string : 패턴을 확인하고자 하는 문자열.

    Returns:
        bool: 주어진 문자열에 패턴이 존재하면 True, 그렇지 않으면 False.
    """
    pattern = r"첨부|연장|결산"
    return bool(re.search(pattern, input_string))

def fill_missing_columns(df : pd.DataFrame, columns_list: list, default_value: str = None):
    """주어진 DataFrame의 누락된 열을 채우는 함수.

    Args:
        df : 열을 채우고자 하는 DataFrame.
        columns_list : 채우고자 하는 열의 이름이 담긴 리스트.
        default_value (optional) : 누락된 열에 채울 기본값. 기본값은 None.

    Returns:
        df (pd.DataFrame) : 열이 채워진 DataFrame.
    """
    missing_columns = set(columns_list) - set(df.columns)
    for col in missing_columns:
        df[col] = default_value
    return df 