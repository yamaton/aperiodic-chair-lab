-- The repository edition keeps relative research links. Pages editions send
-- them to the exact source revision, while the solid viewer is served locally.
function Pandoc(doc)
  local revision = pandoc.utils.stringify(doc.meta.repository_revision)
  local site = pandoc.utils.stringify(doc.meta.site_url)
  local download = pandoc.utils.stringify(doc.meta.edition) == 'download'
  return doc:walk({Link = function(link)
    local target = link.target
    if target:match('^#') or target:match('^[%a][%w+.-]*:') or target:match('^//') then
      return link
    end
    local path, fragment = target:match('^([^#]*)(.*)$')
    local parts = {'docs'}
    for part in path:gmatch('[^/]+') do
      if part == '..' then
        assert(#parts > 0, 'Link escapes the repository: ' .. target)
        table.remove(parts)
      elseif part ~= '.' then
        table.insert(parts, part)
      end
    end
    local relative = table.concat(parts, '/')
    local file = assert(io.open(relative, 'rb'), 'Missing link target: ' .. relative)
    file:close()
    if relative == 'strong/artifacts/recut-chair.html' then
      link.target = (download and (site .. 'viewer/') or '../viewer/') .. fragment
    else
      link.target = 'https://github.com/yamaton/aperiodic-chair-lab/blob/'
        .. revision .. '/' .. relative .. fragment
    end
    return link
  end})
end
