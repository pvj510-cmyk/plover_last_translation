'''
Functionality to repeat output in Plover with Korean Josa support.
'''

import re
from plover.translation import Translator, Translation, Stroke
from plover.formatting import RetroFormatter


DELIM_ARGS = ','

def josa_last_translation(translator: Translator, stroke: Stroke, args: str) -> None:
    translations = translator.get_state().translations
    if not translations:
        return

    last_text = translations[-1].english
    clean_text = re.sub(r'[^가-힣]', '', last_text)
    
    # args가 있으면 그 글자를 쓰고, 없으면 기본값 '를' 사용
    # 예: =josa_ㄹ(통해서) 라고 쓰면 tail은 " 통해서"가 됨
    tail = f" {args}" if args else ""

    if not clean_text:
        suffix = "를" + tail
    else:
        last_char = clean_text[-1]
        suffix = ("을" if (ord(last_char) - 0xAC00) % 28 > 0 else "를") + tail

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
