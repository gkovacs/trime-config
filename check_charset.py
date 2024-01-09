import opencc
import re
converter = opencc.OpenCC('t2s.json')
converter_s2t = opencc.OpenCC('s2t.json')

all_chars = set()
for filename in ['jyut6ping3.chars.dict.yaml', 'terra_pinyin.dict.yaml', 'cangjie5_tradsimp.dict.yaml']:
  for line in open(filename, 'rt'):
    if '\t' not in line:
      continue
    line_parts = line.split('\t')
    chars = line_parts[0]
    for c in chars:
      all_chars.add(c)

def is_gbk(c):
  try:
    c.encode('gbk')
    return True
  except:
    return False

def is_gb18030(c):
  try:
    c.encode('gb18030')
    return True
  except:
    return False

def is_cjk_basic(c):
  if re.search(u'[\u4e00-\u9fff]', c):
    return True
  return False

def is_extension_a(c):
  if re.search(u'[\u3400-\u4DBF]', c):
    return True
  return False

def is_extension_b(c):
  if re.search(u'[\u20000-\u2A6DF]', c):
    return True
  return False

ranges = [
  {"from": ord(u"\u3300"), "to": ord(u"\u33ff")},         # compatibility ideographs
  {"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")},         # compatibility ideographs
  {"from": ord(u"\uf900"), "to": ord(u"\ufaff")},         # compatibility ideographs
  {"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")}, # compatibility ideographs
  {'from': ord(u'\u3040'), 'to': ord(u'\u309f')},         # Japanese Hiragana
  {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Katakana
  {"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},         # cjk radicals supplement
  {"from": ord(u"\u4e00"), "to": ord(u"\u9fff")},
  {"from": ord(u"\u3400"), "to": ord(u"\u4dbf")},
  {"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")}, # extension b
  #{"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")}, # extension c
  #{"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")}, # extension d
  #{"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}  # included as of Unicode 8.0
]

ranges_any = [
  {"from": ord(u"\u3300"), "to": ord(u"\u33ff")},         # compatibility ideographs
  {"from": ord(u"\ufe30"), "to": ord(u"\ufe4f")},         # compatibility ideographs
  {"from": ord(u"\uf900"), "to": ord(u"\ufaff")},         # compatibility ideographs
  {"from": ord(u"\U0002F800"), "to": ord(u"\U0002fa1f")}, # compatibility ideographs
  {'from': ord(u'\u3040'), 'to': ord(u'\u309f')},         # Japanese Hiragana
  {"from": ord(u"\u30a0"), "to": ord(u"\u30ff")},         # Japanese Katakana
  {"from": ord(u"\u2e80"), "to": ord(u"\u2eff")},         # cjk radicals supplement
  {"from": ord(u"\u4e00"), "to": ord(u"\u9fff")},
  {"from": ord(u"\u3400"), "to": ord(u"\u4dbf")},
  {"from": ord(u"\U00020000"), "to": ord(u"\U0002a6df")}, # extension b
  #{"from": ord(u"\U0002a700"), "to": ord(u"\U0002b73f")}, # extension c
  #{"from": ord(u"\U0002b740"), "to": ord(u"\U0002b81f")}, # extension d
  #{"from": ord(u"\U0002b820"), "to": ord(u"\U0002ceaf")}  # included as of Unicode 8.0
]

def is_cjk(char):
  return any([range["from"] <= ord(char) <= range["to"] for range in ranges])

def is_cjk_any(char):
  return any([range["from"] <= ord(char) <= range["to"] for range in ranges_any])


# print(converter_s2t.convert('𫗭'))

# print(is_gbk('餵'))
# print(is_cjk_basic('餵'))
# print(is_gb18030('餵'))
# print(converter.convert('餵'))
# print(is_gb18030('𫗭'))
# print(is_cjk_basic('𫗭'))
# print(is_gbk('𫗭'))

trad_to_simp_list = {}

for c in all_chars:
  if not is_cjk_basic(c) or is_extension_a(c):
    continue
  #if not (is_gb18030(c) and (is_cjk_basic(c) or is_extension_a(c) or is_extension_b(c) or is_cjk(c))):
  #  continue
  #if not is_gbk(c):
  #  continue
  c_simp = converter.convert(c)
  if c == c_simp:
    continue
  if c not in trad_to_simp_list:
    trad_to_simp_list[c] = []
  if c_simp not in trad_to_simp_list[c]:
    trad_to_simp_list[c].append(c_simp)

for x in open('TSCharacters.txt', 'rt').readlines():
  c,simp_list = x.split('\t')
  if not is_cjk_basic(c) or is_extension_a(c):
    continue
  for c_simp in simp_list:
    if c_simp.strip() == '':
      continue
    if c not in trad_to_simp_list:
      trad_to_simp_list[c] = []
    if c_simp not in trad_to_simp_list[c] and c_simp != c:
      trad_to_simp_list[c].append(c_simp)

out_set = set()

for c,simp_list in trad_to_simp_list.items():
  valid_simp_list = []
  for c_simp in simp_list:
    if is_cjk_basic(c_simp) and is_gbk(c_simp):
      valid_simp_list.append(c_simp)
  best_simp = None
  if len(valid_simp_list) > 0:
    best_simp = valid_simp_list[0]
  for c_simp in simp_list:
    if is_gbk(c_simp):
      continue
    if best_simp is None:
      out_set.add(f'{c}\t{c}')
      if is_gb18030(c_simp) and (is_cjk_basic(c_simp) or is_extension_a(c_simp) or is_extension_b(c_simp) or is_cjk(c_simp)):
        out_set.add(f'{c_simp}\t{c}')
    else:
      if len(valid_simp_list) == 1:
        out_set.add(f'{c}\t{best_simp}')
      if c_simp != best_simp:
        if is_gb18030(c_simp) and (is_cjk_basic(c_simp) or is_extension_a(c_simp) or is_extension_b(c_simp) or is_cjk(c_simp)):
          out_set.add(f'{c_simp}\t{best_simp}')

stchars = open('opencc/TSCharacters_custom.txt', 'wt')
for x in out_set:
  print(x, file=stchars)
