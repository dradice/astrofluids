--[[
macros.lua -- format-aware math macros for the ASTRO 442 notes.

Why a filter instead of \newcommand: MathJax ignores \mathbf on lowercase
Greek letters (renders them plain italic) and \boldsymbol gives bold
*italic*.  Upright bold Greek in the browser needs the Unicode
"Mathematical Bold" characters (U+1D6C2...), which screen readers announce
as "bold xi".  Typst renders \mathbf{\xi} correctly, so other formats get
plain \mathbf.

Macros:
  \vb{x}   vector, upright bold (Latin and Greek)
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
  -- name = "template with #1"
}

-- TeX name -> Unicode MATHEMATICAL BOLD (upright) code point
local BOLD_GREEK = {
  alpha = 0x1D6C2, beta = 0x1D6C3, gamma = 0x1D6C4, delta = 0x1D6C5,
  varepsilon = 0x1D6C6, zeta = 0x1D6C7, eta = 0x1D6C8, theta = 0x1D6C9,
  iota = 0x1D6CA, kappa = 0x1D6CB, lambda = 0x1D6CC, mu = 0x1D6CD,
  nu = 0x1D6CE, xi = 0x1D6CF, pi = 0x1D6D1, rho = 0x1D6D2,
  varsigma = 0x1D6D3, sigma = 0x1D6D4, tau = 0x1D6D5, upsilon = 0x1D6D6,
  varphi = 0x1D6D7, chi = 0x1D6D8, psi = 0x1D6D9, omega = 0x1D6DA,
  epsilon = 0x1D6DC, vartheta = 0x1D6DD, varkappa = 0x1D6DE,
  phi = 0x1D6DF, varrho = 0x1D6E0, varpi = 0x1D6E1,
  nabla = 0x1D6C1,
}

local is_html = quarto and quarto.doc.is_format("html")

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
  local name = arg:match("^%s*\\(%a+)%s*$")
  if is_html and name and BOLD_GREEK[name] then
    return utf8.char(BOLD_GREEK[name])
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
        local body = ONEARG[name]:gsub("#1", function() return expand(arg) end)
        out[#out + 1] = body
        i = nxt
      elseif SIMPLE[name] then
        out[#out + 1] = SIMPLE[name]
        -- keep TeX semantics: a space after a control word is swallowed
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
