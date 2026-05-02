import re
from plover.translation import Translator, Translation, Stroke

def josa_last_translation(translator: Translator, stroke: Stroke, args: str) -> None:
    translations = translator.get_state().translations
    if not translations:
        return

    # 마지막 단어 가져오기
    last_text = translations[-1].english
    # 한글만 추출 (받침 판별용)
    clean_text = re.sub(r'[^가-힣]', '', last_text)
    
    # 명령어 뒤에 붙은 글자(args)가 있으면 앞에 공백을 포함해 tail로 만듦
    tail = f" {args}" if args else ""

    if not clean_text:
        suffix = "를" + tail
    else:
        last_char = clean_text[-1]
        # 받침 판별 공식
        suffix = ("을" if (ord(last_char) - 0xAC00) % 28 > 0 else "를") + tail

    # 앞 단어와 공백 없이 결합 ({^})
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
