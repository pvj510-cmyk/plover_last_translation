import re
from plover.translation import Translator, Translation, Stroke

def josa_last_translation(translator: Translator, stroke: Stroke, args: str) -> None:
    translations = translator.get_state().translations
    if not translations:
        return

    # 1. 마지막 번역 결과 가져오기 (None 방지 처리)
    last_translation = translations[-1]
    last_text = last_translation.english if last_translation.english is not None else ""

    # 2. 한글만 추출 (받침 판별용)
    clean_text = re.sub(r'[^가-힣]', '', last_text)
    
    # 3. 추가 텍스트(args) 처리
    tail = f" {args}" if args else ""

    # 4. 받침 판별 로직 (텍스트가 비어있으면 기본값 '를')
    if not clean_text:
        suffix = "를" + tail
    else:
        last_char = clean_text[-1]
        # 한글 유니코드 판별 공식
        suffix = ("을" if (ord(last_char) - 0xAC00) % 28 > 0 else "를") + tail

    # 5. 최종 출력
    new_translation = Translation([stroke], "{^" + suffix + "}")
    translator.translate_translation(new_translation)

def repeat_last_translation(translator: Translator, stroke: Stroke, args: str) -> None:
    '''
    Macro to repeat the last translation(s) in Plover.
    '''
    translations = translator.get_state().translations
    if not translations:
        return

    try:
        num_to_repeat = int(args.split(DELIM_ARGS)[0])
    except:
        num_to_repeat = 1

    for translation in translations[-num_to_repeat:]:
        repeated_translation = Translation(translation.strokes, translation.english)
        translator.translate_translation(repeated_translation)

def repeat_last_word(translator: Translator, stroke: Stroke, args: str) -> None:
    '''
    Macro to repeat the last word(s) in Plover.
    '''
    translations = translator.get_state().translations
    if not translations:
        return

    try:
        num_to_repeat = int(args.split(DELIM_ARGS)[0])
    except:
        num_to_repeat = 1

    formatter = RetroFormatter(translations)
    last_words = formatter.last_words(num_to_repeat)

    for word in last_words:
        new_translation = Translation([stroke], word)
        translator.translate_translation(new_translation)

def repeat_last_fragment(translator: Translator, stroke: Stroke, args: str) -> None:
    '''
    Macro to repeat the last fragments(s) in Plover.
    '''
    translations = translator.get_state().translations
    if not translations:
        return

    try:
        num_to_repeat = int(args.split(DELIM_ARGS)[0])
    except:
        num_to_repeat = 1

    formatter = RetroFormatter(translations)
    last_fragments = formatter.last_fragments(num_to_repeat)

    for fragment in last_fragments:
        new_translation = Translation([stroke], fragment)
        translator.translate_translation(new_translation)

def repeat_last_character(translator: Translator, stroke: Stroke, args: str) -> None:
    '''
    Macro to repeat the last character(s) in Plover.
    '''
    translations = translator.get_state().translations
    if not translations:
        return

    try:
        num_to_repeat = int(args.split(DELIM_ARGS)[0])
    except:
        num_to_repeat = 1

    formatter = RetroFormatter(translations)
    last_text = formatter.last_text(num_to_repeat)

    new_translation = Translation([stroke], last_text)
    translator.translate_translation(new_translation)
