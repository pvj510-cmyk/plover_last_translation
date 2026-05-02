'''
Functionality to repeat output in Plover with Korean Josa support.
'''

import re
from plover.translation import Translator, Translation, Stroke
from plover.formatting import RetroFormatter


DELIM_ARGS = ','

def josa_last_translation(translator: Translator, stroke: Stroke, args: str) -> None:
    '''
    Macro to attach Korean Josa (을/를) based on the last translation.
    '''
    # 1. 현재 번역 상태 가져오기
    translations = translator.get_state().translations
    if not translations:
        return

    # 2. 마지막으로 입력된 텍스트 가져오기
    last_translation = translations[-1]
    last_text = last_translation.english

    # 3. 한글 받침 판별 로직
    # 한글만 추출 (특수문자 및 명령어 제거)
    clean_text = re.sub(r'[^가-힣]', '', last_text)
    
    if not clean_text:
        suffix = "를"  # 한글이 없으면 기본값으로 '를' 설정
    else:
        last_char = clean_text[-1]
        # 한글 유니코드 계산법: (한글코드 - 0xAC00) % 28 > 0 이면 받침 있음
        if (ord(last_char) - 0xAC00) % 28 > 0:
            suffix = "을"
        else:
            suffix = "를"

    # 4. 결과 출력 ({^}를 사용하여 앞 단어에 바로 붙임)
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
