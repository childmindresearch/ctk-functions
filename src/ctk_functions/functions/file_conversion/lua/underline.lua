-- Underlines text between "++" and "++" tags.
-- Known bug: Will underline until end of file if no end tag is found.

local in_underline = false

local start_tag = "++"
local end_tag = "++"

return {
    {
        Str = function(elem)
            if in_underline and string.sub(elem.text, -2) == end_tag then
                in_underline = false
                return pandoc.Underline { pandoc.Str(string.sub(elem.text, 1, -3)) }
            elseif in_underline then
                return pandoc.Underline { pandoc.Str(elem.text) }
            elseif string.sub(elem.text, 1, 2) == start_tag and string.sub(elem.text, -2) == end_tag then
                return pandoc.Underline { pandoc.Str(string.sub(elem.text, 3, -3)) }
            elseif string.sub(elem.text, 1, 2) == start_tag then
                in_underline = true
                return pandoc.Underline { pandoc.Str(string.sub(elem.text, 3)) }
            elseif string.sub(elem.text, -2) == end_tag then
                in_underline = false
                return pandoc.Underline { pandoc.Str(string.sub(elem.text, 1, -3)) }
            else
                return elem
            end
        end,
    }
}
