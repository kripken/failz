import random

# Vars

class SimpleVar:
  def __init__(self, pfail):
    self.pfail = pfail

  def sample(self):
    self.value = 1 if random.random() < self.pfail else 0

class ComboVar:
  def __init__(self, sources, pfail):
    self.sources = sources

    sources_pass = 1
    for source in sources:
      sources_pass *= 1 - source.pfail
    sources_fail = 1 - sources_pass

    self.factor = pfail / sources_fail

  def sample(self):
    source_fails = 1 in [source.value for source in self.sources]
    self.value = 1 if source_fails and random.random() < self.factor else 0

# Problems

class Problem:
  def __init__(self):
    self.vars = [SimpleVar(0.5), SimpleVar(0.5)]
    eps = 0.001
    self.vars.append(ComboVar(self.vars[:], 0.5 + eps))

  def sample(self):
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
    means = map(lambda s: s/float(len(self.samples)), sums)
    print means

# Main

a = Analyzer(Problem(), 10000)
a.analyze()

