-- Provides tab support for markdown to docx conversions.

return {
    {
        Str = function(elem)
            local text = elem.text:gsub("%^t", "\t")
            return pandoc.Str(text)
        end,
    }
}
