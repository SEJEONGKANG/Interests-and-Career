import { escapeRegExp } from "lodash";

/**
 * 검색된 기업명을 정규표현식과 Unicode 값을 이용하여 한글 초성 검색 기능을 만들어주는 함수
 * @param {string} ch 검색된 기업명
 * @returns 처리된 기업명
 */
function ch2pattern(ch) {
  const offset = 44032; /* '가'의 코드 */
  // 한국어 음절
  if (/[가-힣]/.test(ch)) {
    const chCode = ch.charCodeAt(0) - offset;
    // 종성이 있으면 문자 그대로를 찾는다.
    if (chCode % 28 > 0) {
      return ch;
    }
    const begin = Math.floor(chCode / 28) * 28 + offset;
    const end = begin + 27;
    return `[\\u${begin.toString(16)}-\\u${end.toString(16)}]`;
  }
  // 한글 자음
  if (/[ㄱ-ㅎ]/.test(ch)) {
    const con2syl = {
      ㄱ: "가".charCodeAt(0),
      ㄲ: "까".charCodeAt(0),
      ㄴ: "나".charCodeAt(0),
      ㄷ: "다".charCodeAt(0),
      ㄸ: "따".charCodeAt(0),
      ㄹ: "라".charCodeAt(0),
      ㅁ: "마".charCodeAt(0),
      ㅂ: "바".charCodeAt(0),
      ㅃ: "빠".charCodeAt(0),
      ㅅ: "사".charCodeAt(0),
    };
    const begin =
      con2syl[ch] ||
      (ch.charCodeAt(0) - 12613) /* 'ㅅ'의 코드 */ * 588 + con2syl["ㅅ"];
    const end = begin + 587;
    return `[${ch}\\u${begin.toString(16)}-\\u${end.toString(16)}]`;
  }
  if (/[\w\d]/.test(ch)) {
    return ch;
  }
  if (/[A-Za-z0-9]/.test(ch)) {
    return ch;
  }

  return escapeRegExp(ch);
}
/**
 * space가 검색창에 들어와도 무시하고 정규표현식 pattern을 반환하여 해당 pattern을 지닌 corplist를 보여주기 위해 만들어진 함수
 * @param {string} input 기업명
 * @returns regex pattern
 */
export function createFuzzyMatcher(input) {
  const withoutSpaces = input.replace(/\s/g, "");
  const pattern = withoutSpaces.split("").map(ch2pattern).join(".*?");
  return new RegExp(pattern, "i");
}
