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

# Main

p = Problem()

for i in range(50):
  print p.sample()
