import re
from plover.translation import Translator, Translation, Stroke

def josa_last_translation(translator: Translator, stroke: Stroke, args: str) -> None:
    translations = translator.get_state().translations
    if not translations:
        return

    # 마지막 번역 결과 가져오기 (None 방지 처리)
    last_translation = translations[-1]
    last_text = last_translation.english if last_translation.english is not None else ""

    # 한글만 추출 (받침 판별용)
    clean_text = re.sub(r'[^가-힣]', '', last_text)
    
    # 추가 텍스트(args) 처리 (예: "통해서")
    tail = f" {args}" if args else ""

    if not clean_text:
        # 한글이 아니거나(숫자 등) 받침이 없는 경우 기본값 '를'
        suffix = "를" + tail
    else:
        last_char = clean_text[-1]
        # 한글 유니코드 판별 공식 (받침 있으면 '을', 없으면 '를')
        suffix = ("을" if (ord(last_char) - 0xAC00) % 28 > 0 else "를") + tail

    # 앞 단어와 공백 없이 결합 ({^})
    new_translation = Translation([stroke], "{^" + suffix + "}")
    translator.translate_translation(new_translation)
