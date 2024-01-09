local charset = require("charset")
charset_filter = charset.filter
charset_comment_filter = charset.comment_filter

-- reverse_lookup_filter: 依地球拼音为候选项加上带调拼音的注释
-- 详见 `lua/reverse.lua`
reverse_lookup_filter_jyutping = require("reversejyutping")
reverse_lookup_filter_jyutping_if_empty = require("reversejyutpingifempty")
