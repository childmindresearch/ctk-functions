-- Provides tab support for markdown to docx conversions.
-- Pandoc automatically converts all consecutives tabs and spaces to a single space,
-- so we need to rely on a custom charater (^t) to represent a tab in the markdown file.

return {
    {
        Str = function(elem)
            local text = elem.text:gsub("%^t", "\t")
            return pandoc.Str(text)
        end,
    }
}
