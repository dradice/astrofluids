--[[
macros.lua -- math macros for the ASTRO 442 notes.

The macros are expanded here, once, for every output format (MathJax HTML
and Typst PDF), so chapters never need \newcommand.

Macros:
  \vb{x}   vector, bold. Latin letters are upright (\mathbf); Greek letters
           and other symbols use \boldsymbol (bold italic), as in the LaTeX
           physics package: \vb{v} -> \mathbf{v}, \vb{\xi} -> \boldsymbol{\xi}
  \dd      upright differential d
  \ii      upright imaginary unit i
  \ee      upright Euler number e

To add a macro, extend SIMPLE (no arguments) or ONEARG (one argument; #1).
]]

local SIMPLE = {
  dd = "\\mathrm{d}",
  ii = "\\mathrm{i}",
  ee = "\\mathrm{e}",
}

local ONEARG = {
  -- name = "template using #1", e.g.  avg = "\\left\\langle #1 \\right\\rangle",
}

-- Read a macro argument starting at position i (after optional spaces):
-- either a balanced {...} group or a single token. Returns arg, next index.
local function read_arg(s, i)
  i = s:find("%S", i) or (#s + 1)
  local c = s:sub(i, i)
  if c == "{" then
    local depth, j = 0, i
    while j <= #s do
      local ch = s:sub(j, j)
      if ch == "\\" then
        j = j + 1
      elseif ch == "{" then
        depth = depth + 1
      elseif ch == "}" then
        depth = depth - 1
        if depth == 0 then return s:sub(i + 1, j - 1), j + 1 end
      end
      j = j + 1
    end
    error("macros.lua: unbalanced braces in: " .. s)
  elseif c == "\\" then
    local name = s:match("^\\%a+", i) or s:sub(i, i + 1)
    return name, i + #name
  else
    return c, i + 1
  end
end

local function vb(arg)
  if arg:match("\\%a") then
    return "\\boldsymbol{" .. arg .. "}"
  end
  return "\\mathbf{" .. arg .. "}"
end

local function expand(s)
  local out, i = {}, 1
  while i <= #s do
    local a, b, name = s:find("^\\(%a+)", i)
    if a then
      if name == "vb" then
        local arg, nxt = read_arg(s, b + 1)
        out[#out + 1] = vb(expand(arg))
        i = nxt
      elseif ONEARG[name] then
        local arg, nxt = read_arg(s, b + 1)
        out[#out + 1] = ONEARG[name]:gsub("#1", function() return expand(arg) end)
        i = nxt
      elseif SIMPLE[name] then
        out[#out + 1] = SIMPLE[name]
        i = b + 1
      else
        out[#out + 1] = s:sub(a, b)
        i = b + 1
      end
    elseif s:sub(i, i) == "\\" then
      out[#out + 1] = s:sub(i, i + 1) -- \\, \{, \, etc.
      i = i + 2
    else
      out[#out + 1] = s:sub(i, i)
      i = i + 1
    end
  end
  return table.concat(out)
end

function Math(el)
  el.text = expand(el.text)
  return el
end
