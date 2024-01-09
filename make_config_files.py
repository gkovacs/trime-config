import ruamel.yaml
import sys
from pathlib import Path
yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True

def replace_in_list(l, old_item, new_item):
  found = False
  for i,x in enumerate(l):
    if x == old_item:
      found = True
      l[i] = new_item
  if not found:
    raise Exception('did not find in list:', old_item)

def insert_after(l, ref_item, new_item):
  for i,x in enumerate(l):
    if x == ref_item:
      l.insert(i+1, new_item)
      return

x = yaml.load(Path('double_pinyin_flypy_simp_show_jyutping.schema.yaml'))
x['schema']['name'] = '雙拼顯粵'
x['schema']['schema_id'] = 'double_pinyin_flypy_show_jyutping'
x['switches'][2]['reset'] = 0
x['schema']['dependencies'].remove('terra_pinyin_simp')
x['schema']['dependencies'].remove('td_pinyin_flypy_simp')
x['putonghua_to_cangjie5_lookup']['dictionary'] = 'terra_pinyin'
x['putonghua_to_cangjie5_lookup']['prism'] = 'td_pinyin_flypy'
x['key_binder']['bindings'][0]['select'] = 'double_jyutping_ext'
yaml.dump(x, Path('double_pinyin_flypy_show_jyutping.schema.yaml'))

extra = yaml.load(Path('show_tones_base.yaml'))

x = yaml.load(Path('double_pinyin_flypy_simp_show_jyutping.schema.yaml'))
x['schema']['name'] = '双拼显调'
x['schema']['schema_id'] = 'double_pinyin_flypy_simp_show_tones'
replace_in_list(x['schema']['dependencies'], 'jyut6ping3_tradsimp_nospaces', 'terra_pinyin_simp_nospaces')
#replace_in_list(x['engine']['segmentors'], 'affix_segmentor@putonghua_to_jyutping_lookup', 'affix_segmentor@putonghua_to_tones_lookup')
insert_after(x['engine']['segmentors'], 'abc_segmentor', 'affix_segmentor@putonghua_to_tones_lookup')
#replace_in_list(x['engine']['translators'], 'script_translator@putonghua_to_jyutping_lookup', 'script_translator@putonghua_to_tones_lookup')
insert_after(x['engine']['translators'], 'reverse_lookup_translator', 'script_translator@putonghua_to_tones_lookup')
#replace_in_list(x['engine']['filters'], 'reverse_lookup_filter@putonghua_to_jyutping_reverse_lookup', 'reverse_lookup_filter@putonghua_to_tones_reverse_lookup')
insert_after(x['engine']['filters'], 'uniquifier', 'reverse_lookup_filter@putonghua_to_tones_reverse_lookup')
#x['engine']['filters'].remove('reverse_lookup_filter@putonghua_reverse_lookup')
x['engine']['filters'].remove('lua_filter@reverse_lookup_filter_jyutping')
del x['putonghua_reverse_lookup']
#del x['putonghua_to_jyutping_lookup']
#del x['putonghua_to_jyutping_reverse_lookup']
x['putonghua_to_tones_lookup'] = extra['putonghua_to_tones_lookup']
x['putonghua_to_tones_reverse_lookup'] = extra['putonghua_to_tones_reverse_lookup']
#del x['recognizer']['patterns']['putonghua_to_jyutping_lookup']
x['recognizer']['patterns']['putonghua_to_tones_lookup'] = "^[a-z]*$"
x['switches'][2]['reset'] = 1
x['key_binder']['bindings'][0]['select'] = 'double_jyutping_shumianyu_simp_ext'
yaml.dump(x, Path('double_pinyin_flypy_simp_show_tones.schema.yaml'))

x['schema']['name'] = '雙拼顯調'
x['schema']['schema_id'] = 'double_pinyin_flypy_show_tones'
x['switches'][2]['reset'] = 0
x['schema']['dependencies'].remove('terra_pinyin_simp')
x['schema']['dependencies'].remove('td_pinyin_flypy_simp')
x['putonghua_to_cangjie5_lookup']['dictionary'] = 'terra_pinyin'
x['putonghua_to_cangjie5_lookup']['prism'] = 'td_pinyin_flypy'
x['key_binder']['bindings'][0]['select'] = 'double_jyutping_shumianyu_ext'
yaml.dump(x, Path('double_pinyin_flypy_show_tones.schema.yaml'))

x = yaml.load(Path('double_jyutping_simp_ext.schema.yaml'))
x['schema']['name'] = '粵雙拼'
x['schema']['schema_id'] = 'double_jyutping_ext'
x['switches'][2]['reset'] = 0
x['schema']['dependencies'].remove('jyut6ping3_simp')
x['schema']['dependencies'].remove('double_jyutping_simp')
x['jyutping_to_cangjie5_lookup']['dictionary'] = 'jyut6ping3'
x['jyutping_to_cangjie5_lookup']['prism'] = 'double_jyutping'
x['key_binder']['bindings'][0]['select'] = 'double_pinyin_flypy_show_jyutping'
yaml.dump(x, Path('double_jyutping_ext.schema.yaml'))

x = yaml.load(Path('double_jyutping_simp_ext.schema.yaml'))
x['schema']['name'] = '粤双拼书'
x['schema']['schema_id'] = 'double_jyutping_shumianyu_simp_ext'
replace_in_list(x['schema']['dependencies'], 'jyut6ping3', 'jyut6ping3_shumianyu')
replace_in_list(x['schema']['dependencies'], 'double_jyutping', 'double_jyutping_shumianyu')
x['translator']['dictionary'] = 'jyut6ping3_shumianyu'
x['translator']['prism'] = 'double_jyutping_shumianyu'
x['switches'][2]['reset'] = 1
x['key_binder']['bindings'][0]['select'] = 'double_pinyin_flypy_simp_show_tones'
yaml.dump(x, Path('double_jyutping_shumianyu_simp_ext.schema.yaml'))

x['schema']['name'] = '粵雙拼書'
x['schema']['schema_id'] = 'double_jyutping_shumianyu_ext'
x['switches'][2]['reset'] = 0
x['schema']['dependencies'].remove('jyut6ping3_simp')
x['schema']['dependencies'].remove('double_jyutping_simp')
x['jyutping_to_cangjie5_lookup']['dictionary'] = 'jyut6ping3'
x['jyutping_to_cangjie5_lookup']['prism'] = 'double_jyutping'
x['key_binder']['bindings'][0]['select'] = 'double_pinyin_flypy_show_tones'
yaml.dump(x, Path('double_jyutping_shumianyu_ext.schema.yaml'))
