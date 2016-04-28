from yandex_translate import YandexTranslate
import language_codes

if __name__ == "__main__":
  translate = YandexTranslate('trnsl.1.1.20160421T051442Z.3f43d13c5d30c594.bf3c396e87421e06cac7eab7b3771b3bf20af85c')
  print ":speak: What do you want to translate?"
  print ":listen:"
  message = raw_input()
  print "Translating {}".format(message)
  language = translate.detect(message)
  # translate from detected language to english
  print ":speak:You are speaking {}".format(language_codes.languages[language])
  translation = translate.translate(message, '{}-en'.format(language))
  print translation
  print ":speak:The english translation is {}".format(translation["text"][0])