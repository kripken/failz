import random

# Vars

class Var:
  def __init__(self):
    self.clear()

  def clear(self):
    self.value = None

class SimpleVar(Var):
  def __init__(self, pfail):
    self.clear()

    self.pfail = pfail

  def sample(self):
    if self.value is not None: return
    self.value = 1 if random.random() < self.pfail else 0

class ComboVar(Var):
  def __init__(self, sources, pfail):
    self.clear()

    self.sources = sources

    sources_pass = 1
    for source in sources:
      sources_pass *= 1 - source.pfail
    sources_fail = 1 - sources_pass

    self.factor = pfail / sources_fail

  def sample(self):
    for source in self.sources: source.sample()
    source_fails = 1 in [source.value for source in self.sources]
    self.value = 1 if source_fails and random.random() < self.factor else 0

# Problems

class Problem:
  def __init__(self, smart):
    base = 0.01
    good = []
    bad = []
    for i in range(10):
      x = SimpleVar(base)
      y = SimpleVar(base)
      z = ComboVar([x, y], base * 1.0001)
      good += [x, y]
      bad += [z]
    if smart:
      self.vars = good + bad
    else:
      self.vars = bad + good

  def sample(self):
    for var in self.vars: var.clear()
    for var in self.vars: var.sample()
    return [var.value for var in self.vars]

# Analyzer

class Analyzer:
  def __init__(self, problem, n):
    self.samples = [problem.sample() for i in range(n)]
    #print self.samples

  def analyze(self):
    sums = [0]*len(self.samples[0])
    for s in self.samples:
      for i in range(len(sums)):
        sums[i] += s[i]
    self.means = map(lambda s: s/float(len(self.samples)), sums)
    #print self.means

  def estimate(self):
    l = 0
    for sample in self.samples:
      if 1 in sample:
        #l += sample.index(1) + 1
        l += (sample.index(1) + 1)**2
    self.loss = l/float(len(self.samples))
    return self.loss

# Main

N = 100000

a = Analyzer(Problem(True), N)
a.analyze()
smart = a.estimate()
print 'smart:', smart

a = Analyzer(Problem(False), N)
a.analyze()
dumb = a.estimate()
print 'dumb:', dumb

print 'factor:', dumb/smart

