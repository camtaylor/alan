from yandex_translate import YandexTranslate
import language_codes

if __name__ == "__main__":
  translate = YandexTranslate('trnsl.1.1.20160420T042838Z.0193c4312e09c1cf.28565b33bc14f4fa16679cf7e0315dfa81d66166')
  print ":speak: What do you want to translate?"
  print ":listen:"
  message = raw_input()
  print "Translating {}".format(message)
  language = translate.detect(message)
  # translate from detected language to english
  print ":speak:You are speaking {}".format(language_codes.languages[language])
  translation = translate.translate(message, '{}-en'.format(language))
  print ":speak:The english translation is {}".format(translation["text"][0])