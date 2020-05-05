#!/usr/bin/python3

#An implementation of Tailor in Python.
#Tailor, and this interpreter, is by cyanidesDuality.
#Much help was provided by LyricLy.

import ast
import re
import sys

if len(sys.argv) < 2:
	print("Usage: tailor <file>")
	sys.exit(-1)

program = open(sys.argv[1]).read();


def ansify(s,esc):
	return ("\u001b[38;5;" + str(esc) + "m" + s + "\u001b[0m")

# program = """
# #Program for reversing given fabric
# procedure shunt (fabric1, fabric2) {
# 	move fabric1 -p /./ fabric2
# 	alter fabric1 - /./ ""
# }

# procedure reverse (fabric){
# 	condition some = fabric - /./ update
# 	embroider revfab - ""
# 	while some {
# 		do shunt (fabric, revfab)
# 	}
# 	move revbuff - // fabric
# }

# gather
# copy materials reversing
# do reverse (reversing)
# copy reversing garment
# sell
# """
# program = """
# #Program for signum; breaks with decimals between 0 and 1, and numbers with leading zeroes
# gather
# move materials - /./ cut
# alter cut - /-/ "-1"
# alter cut - /[2-9]/ "1"
# move cut - // garment
# sell
# """

program_split = program.split("\n")
program_split = [l.strip() for l in program_split if not(l == "" or l[0] == "#")]
tokenised = []
sspecial = ["[","(","]",")"]
special = sspecial + ["'",'"',"/"]


def flaglist(s):
	s = s.strip("-")
	return [i for i in s]
for l in program_split:
	parsing = l+" "
	line = []
	while parsing != "":
		if parsing[0] in special:
			if parsing[0] in sspecial:
				index = sspecial.index(parsing[0])+2
				char = sspecial[index]
				find = parsing.index(char)
				cut = parsing[:find]
				cut = cut[1:]
				if parsing[0] == "(":
					array = cut.split(',')
					array = [a.strip() for a in array]
				else:
					cut = cut[1:-1]
					array = cut.split('","')
				parsing = parsing[find+1:]
				line.append(array)
			else:
				space = parsing.index(parsing[0],1)
				line.append(parsing[:space+1].strip(parsing[0]))
				parsing = parsing[space+2:]
		else:
			space = parsing.index(" ")
			line.append(parsing[:space])
			parsing = parsing[space+1:]
	tokenised.append(line)

def updateBool(name, boollist, bufflist):
	updating = boollist[name]
	code = updating["code"]
	if code[1][0] == "-":
		try:
			frbuff = bufflist[code[0]]
		except KeyError:
			return False
		reflags = [getattr(re,f) for f in flaglist(code[1])]
		regex = code[2]
		reflag = False
		for f in reflags:
			reflag == reflag | f
		matches = re.findall(regex, frbuff, reflag)
		boollist[name]["value"] = len(matches) > 0
	elif code[0] == "not":
		try:
			invert = boollist[code[1]]["value"]
		except KeyError:
			return False
		boollist[name]["value"] = not invert
	else:
		try:
			bool0 = boollist[code[0]]["value"]
		except KeyError:
			return False
		try:
			bool1 = boollist[code[1]]["value"]
		except KeyError:
			return False
		if code[1] == "or":
			boollist[name]["value"] = bool0 or bool1
		elif code[1] == "and":
			boollist[name]["value"] = bool0 and bool1
		elif code[1] == "xor":
			boollist[name]["value"] = bool0 != bool1
		else:
			boollist[name]["value"] == False
	return True

def getval(name, key, frame, default, outscope=True, ignore=False):
	if name == "garment" and key == "buffers" and not ignore:
		return default
	if frame == None:
		return default
	try:
		checking = frame[key]
	except KeyError:
		return default
	try:
		val = checking[name]
	except KeyError:
		if outscope:
			val = getval(name,key,frame["parent"],default)
		else:
			val = default
	return val
def writeval(name, key, frame, value, base=True, outscope=True):
	if name == "materials" and key == "buffers":
		return None
	if frame == None:
		return None
	try:
		checking = frame[key]
	except KeyError:
		return
	try:
		val = checking[name]
	except KeyError:
		if outscope:
			p = writeval(name,key,frame["parent"],value,base=False,outscope=outscope)
			if p == "Successful":
				return "Successful"
			elif base:
				frame[key][name] = value
				return None
			else:
				return None
		else:
			frame[key][name] = value
			return None
	frame[key][name] = value
	return "Successful"

def updateDeep(frame,key):
	if frame == None:
		return None
	checkframe = frame
	while checkframe != None:
		updated = updateBool(key, frame['bools'], checkframe['buffers'])
		print(checkframe)
		print(updated)
		if updated:
			return
		checkframe = checkframe['parent']

def updateAllDeep(frame):
	if frame == None:
		return None
	for key, value in frame['bools'].items():
		if value["update"]:
			updateDeep(frame,key)


def interpret(tointerpret,debug,prevframe,prevargs={}):
	frame = {
		"pointer" : 0,
		"buffers" : {"materials": "", "garment": ""},
		"labels" : {},
		"classes" : {},
		"functions" : {},
		"bools" : {},
		"loops" : [],
		"parent" : prevframe
	}
	for key, value in prevargs.items():
		frame["buffers"][key] = value
	while frame["pointer"] < len(tointerpret):
		line = tointerpret[frame["pointer"]] 
		command = line[0]
		if debug:
			print("\n\n\n")
			print("Procedures:",frame['functions'])
			print("Notches:",frame['labels'])
			print("Types:",frame['classes'])
			print("Fabrics:",frame['buffers'])
			print("Conditions:",frame['bools'])
			print("Current command:",command)
			print("Current line:\n",line)
			wait = input("Press Enter key to continue, or press any key and enter to stop execution.\n")
			if wait:
				sys.exit(0)


		if command == "notch":
			writeval(line[1], "labels", frame, pointer, outscope=False)




		elif command == "end":
			frame["pointer"] = len(tointerpret)




		elif command == "see":
			try:
				frame["pointer"] = int(line[1])
			except ValueError:
				frame["pointer"] = getval(line[1], "labels", frame, frame["pointer"] + 1)




		elif command == "if":
			check = getval(line[1], "bools", frame, False)["value"]
			if check:
				frame["pointer"] += 1
				frame["loops"].append("if")
			else:
				counter = 1
				frame["pointer"] += 1
				while counter != 0:
					if tointerpret[frame["pointer"]][-1] == "{":
						counter += 1
					if tointerpret[frame["pointer"]][0] == "}":
						counter -= 1
					frame["pointer"] += 1
				frame["pointer"] += 1



		elif command == "while":
			check = getval(line[1], "bools", frame, False)["value"]
			if not check:
				counter = 1
				frame["pointer"] += 1
				while counter != 0:
					if tointerpret[frame["pointer"]][-1] == "{":
						counter += 1
					if tointerpret[frame["pointer"]][0] == "}":
						counter -= 1
					frame["pointer"] += 1
			else:
				frame["loops"].append("while")
				frame["pointer"] += 1




		elif command == "}":
			try:
				current = frame["loops"].pop()
			except IndexError:
				current = None
			if current == None:
				frame["pointer"] += 1
			elif current == "if":
				frame["pointer"] += 1
			elif current == "while":
				counter = 1
				frame["pointer"] -= 1
				while counter != 0:
					if tointerpret[frame["pointer"]][-1] == "{":
						counter -= 1
					if tointerpret[frame["pointer"]][0] == "}":
						counter += 1
					frame["pointer"] -= 1
				frame["pointer"] += 1




		elif command == "condition":
			try:
				update = line[6] == "update"
			except IndexError:
				update = False
			code = line[3:]
			if update:
				code = line[3:-1]
			writeval(line[1], "bools", frame, {
				"update": update,
				"value": None,
				"code": code
			})
			updateDeep(frame, line[1])
			frame["pointer"] += 1




		elif command == "embroider":
			if len(line) == 4:
				string = line[3]
			else:
				string = line[2]
			if len(line) == 4:
				flags = [f for f in flaglist(line[2]) if f in ["a","p"]]
			else:
				flags = []
			if "a" in flags:
				writeval(line[1], "buffers", frame, getval(line[1], "buffers", frame, "",ignore=True) + string)
			elif "p" in flags:
				writeval(line[1], "buffers", frame, string + getval(line[1], "buffers", frame, "", ignore=True))
			else:
				writeval(line[1], "buffers", frame, string)
			frame["pointer"] += 1



		elif command == "gather":
			frame["buffers"]["materials"] = input("Pattern Input: ")
			frame["pointer"] += 1


		elif command == "hem":
			writeval(line[1], "buffers", frame, ast.literal_eval('"'+getval(line[1], "buffers", frame, "")+'"'))
			frame["pointer"] += 1


		elif command == "sell":
			print(frame["buffers"]["garment"])
			writeval("garment", "buffers", frame, "")
			frame["pointer"] += 1



		elif command == "dye":
			try:
				esc = int(line[2])
			except ValueError:
				try:
					buff = frame['buffers'][line[2]]
				except KeyError:
					buff = 255
				try:
					esc = int(buff)
				except ValueError:
					esc = 255
			writeval(line[1], "buffers", frame, re.sub(r"\x1b\[38;5;[0-9]+m","",getval(line[1], "buffers", frame, "", ignore = True)))
			writeval(line[1], "buffers", frame, re.sub(r"\x1b\[0m","",getval(line[1], "buffers", frame, "", ignore = True)))
			writeval(line[1], "buffers", frame, ansify(getval(line[1], "buffers", frame, "", ignore = True),esc))
			frame['pointer'] += 1


		elif command == "bleach":
			writeval(line[1], "buffers", frame, re.sub(r"\x1b\[38;5;[0-9]+m","",getval(line[1], "buffers", frame, "", ignore = True)))
			writeval(line[1], "buffers", frame, re.sub(r"\x1b\[0m","",getval(line[1], "buffers", frame, "", ignore = True)))
			frame['pointer'] += 1


		elif command == "stop":
			sys.exit(0)


		elif command == "procedure":
			counter = 1
			pos = frame['pointer'] + 1
			while counter > 0 and pos < len(tointerpret):
				if tointerpret[pos][0] == "}":
					counter -= 1
				if len(tointerpret[pos]) > 2:
					if tointerpret[pos][-1] == "{":
						counter += 1
				pos += 1
			pos -= 1
			if len(tointerpret[pos]) > 0:
				if tointerpret[pos][0] == "}":
					pos -= 1
			code = tointerpret[frame['pointer']+1:pos+1]
			writeval(line[1], "functions", frame, {"arguments":line[2],"code":code})
			frame['pointer'] = pos + 2



		elif command == "type":
			linec = line[:]
			linec = linec[3:]
			classadd = []
			for i in linec:
				if i == "+":
					continue
				elif isinstance(i, list):
					classadd += i
				else:
					add = getval(i, "classes", frame, i)
					classadd += add
			writeval(line[1], "classes", frame, classadd)
			frame['pointer'] += 1


		elif command == "replace":
			buffi = line[1]
			buff = getval(buffi, "buffers", frame, "", ignore=True)
			flags = flaglist(line[2]) if len(line) == 5 else []
			fr = line[3] if len(line) == 5 else line[2]
			frclass = getval(fr, "classes", frame, [])
			to = line[4] if len(line) == 5 else line[3]
			toclass = getval(to, "classes", frame, [])
			tempbuff = ""
			if "g" in flags:
				times = -1
			else:
				times = 1
			for c in range(len(buff)):
				char = buff[c]
				if times == 0:
					tempbuff = tempbuff + char
					continue
				add = ""
				if char in frclass:
					idx = frclass.index(char)
					try:
						replace = toclass[idx]
					except IndexError:
						replace = ""
					if "a" in flags:
						add = char + replace
					elif "p" in flags:
						add = replace + char
					else:
						add = replace
					times -= 1
				else:
					add = char
				tempbuff += add
			writeval(buffi, "buffers", frame, tempbuff)
			frame['pointer'] += 1



		elif command == "copy":
			fr = line[1]
			frbuff = getval(fr, "buffers", frame, "")
			to = line[4] if len(line) == 5 else line[2]
			tobuff = getval(to, "buffers", frame, "", ignore=True)
			flags = flaglist(line[2]) if len(line) == 5 else []
			regex = line[3] if len(line) == 5 else ""
			if flags == [] and regex == "":
				writeval(to, "buffers", frame, frbuff)
				frame['pointer'] += 1
				continue
			elif regex != "":
				flags2 = flags[:]
				flags2 = [f for f in flags2 if f not in ["a","p","g"]]
				reflags = [getattr(re,f) for f in flags2]
				try:
					reflag = reflags[0]
				except IndexError:
					reflag = 0
				for f in reflags:
					reflag = reflag | f
				matches = re.findall(regex, frbuff, reflag)
				add = ""
				if "g" in flags:
					add = "".join(matches)
				else:
					try:
						add = matches[0]
					except IndexError:
						add = ""
				if "a" in flags:
					writeval(to, "buffers", frame, tobuff+add)
				elif "p" in flags:
					writeval(to, "buffers", frame, add+tobuff)
				else:
					writeval(to, "buffers", frame, add)
				frame['pointer'] += 1
			else:
				writeval(to, "buffers", frame, "")
				frame['pointer'] += 1
				continue




		elif command == "alter":
			fr = line[1]
			frbuff = getval(fr, "buffers", frame, "")
			to = line[4]
			flags = flaglist(line[2])
			regex = line[3]
			if flags == [] and regex == "":
				writeval(fr, "buffers", frame, to)
				frame['pointer'] += 1
				continue
			elif regex != "":
				flags2 = flags[:]
				flags2 = [f for f in flags2 if f not in ["a","p","g"]]
				reflags = [getattr(re,f) for f in flags2]
				try:
					reflag = reflags[0]
				except IndexError:
					reflag = 0
				for f in reflags:
					reflag = reflag | f
				matchstart = [m.start() for m in re.finditer(regex, frbuff, reflag)]
				matchend = [m.end() for m in re.finditer(regex, frbuff, reflag)]
				matches = [frbuff[matchstart[i]:matchend[i]] for i in range(len(matchstart))]
				replaces = [re.sub(regex,to,m) for m in matches]
				tries = 1
				if "g" in flags:
					tries = -1
				char = 0
				build = ""
				while char < len(frbuff):
					if char in matchstart:
						idx = matchstart.index(char)
						if tries != 0:
							if "a" in flags:
								build += matches[idx]
								build += replaces[idx]
								char = matchend[idx] - 1
							elif "p" in flags:
								build += replaces[idx]
								build += matches[idx]
								char = matchend[idx] - 1
							else:
								build += replaces[idx]
								char = matchend[idx] - 1
							tries -= 1
						else:
							build += frbuff[char]
					else:
						build += frbuff[char]
					char += 1
				writeval(fr, "buffers", frame, build)
			frame['pointer'] += 1
		elif command == "do":
			func = getval(line[1], "functions", frame, "")
			code = func["code"][:]
			args = func["arguments"]
			params = line[2]
			funcin = {}
			i = 0
			for key in params:
				funcin[args[i]] = frame["buffers"][key]
				i += 1
			interpret(code, True, frame, prevargs=funcin)
			i = 0
			for key in params:
				frame["buffers"][key] = funcin[args[i]]
				i += 1
			frame['pointer'] += 1
		else:			
			frame['pointer'] += 1

		updateAllDeep(frame)
	for key, value in prevargs.items():
		prevargs[key] = frame["buffers"][key]





interpret(tokenised, False, None)