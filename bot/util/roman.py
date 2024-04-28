def roman(num: int):
  lookup = [
    (10, 'X'),
    (9, 'IX'),
    (5, 'V'),
    (4, 'IV'),
    (1, 'I'),
  ]

  res = ""

  for (n, roman) in lookup:
    (d, num) = divmod(num, n)
    res += roman * d

  return res