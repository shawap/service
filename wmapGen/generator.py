import onnx
import numpy as np


fpath = './mnist16x16x16.onnx'
# fpath = './mnist256x256x256.onnx'
model = onnx.load(fpath)


inits = []
for init in model.graph.initializer :
    inits.append(init)

weights_bias = len(inits)
print("weights + bias : {}".format(weights_bias))


layerdim = []
for i in range(0, weights_bias):
    if i == weights_bias - 1:
        #print(inits[i].dims[0])
        layerdim.append(inits[i].dims[0])
    elif i % 2 == 0:
        #print(inits[i].dims[0])
        layerdim.append(inits[i].dims[0])

print("Structure of each layer : {}".format(layerdim))


numOfLayer = len(layerdim)
numOfGap = numOfLayer - 1
maxLayer = max(layerdim[:])
dimOfLayer = str(layerdim).replace('[', '{').replace(']', '}')

coef = []

for i in inits:
    coef += (list(i.double_data))

coef = str(coef).replace('[','{ ').replace(']',' }')

with open('./template.c', 'r') as fp:
    ccode = fp.readlines()

outputs = ''
for cline in ccode:
    outputs += cline

outputs = outputs.format(numOfLayer, numOfGap, maxLayer, '(int [])' + dimOfLayer, coef).replace('lbrace', '{').replace('rbrace', '}')
with open('result.c', 'w') as fp:
    fp.write(outputs)
