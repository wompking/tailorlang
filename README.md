# Tailor
A string-based esoteric programming language.

## Table Of Contents
* [Introduction](#introduction)
* [Syntax and Terms](#syntax-and-terms)
* [Frames and Procedures](#frames-and-procedures)
* [Commands](#commands)
* [Installing](#installing)
* [Acknowledgments](#acknowledgments)

## Introduction
Tailor is a string-based esoteric programming language. As such, it is not recommended to program anything involving numeric calculations in Tailor. It *could* be used to program text adventure games, but come on. Do you *really* think you can code something worthwhile in this? File extensions for Tailor patterns are `.tl` or `.tail`. Tailor is *forgiving*; any errors or unknown commands are handled by skipping over the error like the command that caused the error never existed. Tailor officially recognises the `#` character as its comment; however, because of the forgiving behavior detailed above, as long as a line doesn't start with a Tailor command it can be treated like a comment.

## Syntax and Terms
Tailor introduces some unique syntax for its programs; this is to make the language more esoteric.  
Tailor *fabrics* are the equivalent of variables; they can store one string.  
Tailor *conditions* are the equivalent of Boolean variables; they can store one value which can be `true` or `false`.  
Tailor *patterns* are the equivalent of programs.  
Tailor *procedures* are the equivalent of functions.  
A *Tailor* is the person creating a Tailor pattern; this is not to be confused with Tailor itself.  

## Frames and Procedures
A frame contains all the information in a Tailor pattern. Whenever anything is created in a Tailor pattern, like a fabric or a condition, it is stored in the current frame. When a procedure is called, it creates a new frame whose parent is the previous frame; the arguments the procedure is passed are stored in the new frame as well. 

For example, if there is a fabric, `foo`, and procedure `f` with argument `x` is called with `foo`, then the value of `foo` is copied out of the current frame and copied into the new frame *under the name of `x`.* Values referenced in commands are always checked at the highest level first; in the previous example, if a fabric, `x`, was present in the outermost frame, the procedure would switch from rewriting the fabric `foo` that was *renamed* to `x` to rewriting the fabric `x`. 

Note that the names of fabrics are never actually changed in a Tailor pattern. During a procedure, fabrics are *not actually changed*; only their "alias fabrics" are, and the values are copied back after execution.

## Commands

In this table, required arguments are shown in ***bold italic*** and optional arguments are shown in **regular bold**.

| Name and Usage      | Function |
|---------------------|----------|
| gather              | Takes input from the user and stores it in fabric `materials`. |
| sell                | Takes fabric `garment`, prints it, and clears it. |
| stop                | Halts program execution. |
| end                 | Halts execution of current procedure; behaves like `stop` command if not in a procedure. Does *not* exit out of `while` loops. |
| notch ***name***    | Creates a notch with name ***name*** that can be used in `see` commands.|
| see ***position***  | If ***position*** is an integer, this command goes to line number ***position.*** Otherwise, this command goes to the notch with name ***position.***
| hem ***name***      | Interprets fabric with name ***name*** as Unicode; for example, `foo\u2756bar` would become `foo❖bar`.
| condition ***name*** = ***fabric flags regex*** **update** | Checks if ***fabric*** matches ***regex*** with ***flags*** and creates a new condition, ***name,*** with the value of that expression. If update is set, this is updated after each pattern step; otherwise, it is evaluated once and its value is then not changed if the referenced fabric changes. For example, `condition foo = checking - /A/ update` checks whether fabric `checking` has any occurrences of the string `A` in it, and sets condition `foo` accordingly, updating each pattern step.
| condition ***name*** = not ***condition*** **update** | Should be self-explanatory.
| condition ***name*** = ***fabric 1*** == ***fabric 2*** **update** | Checks if ***fabric 1*** and ***fabric 2*** are equal.
| condition ***name*** = ***condition 1*** ***operation*** ***condition 2*** **update** | Should be self-explanatory. Supported operations are `and`, `or`, and `xor`.
| if ( ***condition*** ){|Checks if ***condition*** is true and executes code block accordingly. The parentheses are optional.
| while ( ***condition*** ){|Loops while ***condition*** is true. The parentheses are optional.
| bleach ***fabric*** | Strips ***fabric*** of any ANSI color codes.
| dye ***fabric color*** |If ***color*** is an integer, this command colors ***fabric*** with the corresponding ANSI color code. Otherwise, the color code used is the value of the fabric ***color.*** In this case, if ***color*** is not a valid fabric or the value of ***color*** is not an integer, the color code used is `255` instead.
| embroider ***fabric*** **flags** ***string*** | Writes ***string*** to ***fabric.*** Supported flags are `a` and `p`, which respectively append and prepend ***string*** to ***fabric*** instead of overwriting it. In case of `-ap`, both are applied and ***fabric*** is "wrapped" with ***string.***
| copy ***fabric 1*** **flags regex** ***fabric 2*** | Copies the parts of ***fabric 1*** that match **regex** with **flags** to ***fabric 2.*** The `a` and `p` flags mentioned before can also additionally be set. Note that **flags** and **regex** come as a set; either both **flags** and **regex** are included or neither are.
| type ***name*** = ***contents*** | Creates a new type with name ***name*** and contents ***contents.*** For example, `type vowels = ["a","e","i","o","u"]` creates a new type named `vowels` with the contents `"a","e","i","o","u"`. **ALWAYS** use double quotes.
| type ***name*** = ***type 1*** + ***type 2*** | Creates a new type with name ***name*** and with contents equal to ***type 1*** prepended to ***type 2.*** Using the previous example, `type vowelY = vowels + ["y"]` creates a new type with the contents `"a","e","i","o","u","y"`, and `type foo = vowels + vowelY` creates a new type with the contents `"a","e","i","o","u","y","a","e","i","o","u"`
| replace ***fabric*** **flags** ***type 1 type 2*** | Goes through ***fabric*** and replaces all occurrences of a character from ***type 1*** with the corresponding character from ***type 2.*** Supported flags are `a`,`p`, and `g`. `g` is the global flag; without it, only the first occurrence is replaced.
| alter ***fabric flags regex replace*** | Finds all occurrences of ***regex*** with ***flags*** in ***fabric*** and replaces them with string ***replace.***  If both ***flags*** and ***regex*** are empty, this command acts like `embroider fabric replace`. Supported flags are `a`,`p`, and `g`.
| procedure ***name*** ( ***arguments*** ){ | Creates a new procedure, ***name,*** with ***arguments*** whose code is the code block after this command.
| do ***name*** ( ***arguments*** ) | Does procedure ***name*** with ***arguments.***
| variation ***path*** | Imports a file with relative path ***path*** , running it and copying its functions. For example, `variation examples/reversing.tail` would create the functions `reversing.shunt` and `reversing.reverse`, also executing any additional code.

## Installing

Clone this repository or download [tailor.py](https://raw.githubusercontent.com/wompking/tailorlang/master/tailor.py) directly.

Either run using Python (version 3):

```
python3 tailor.py <pattern.tail>
```

Or, ensure that the file is executable and in your `PATH`:

```
tailor.py <pattern.tail>
```


## Acknowledgments
Many thanks go out to [LyricLy](https://github.com/LyricLy) for showing me how to do regular expressions in Python and general help, and to [tripodsan](https://github.com/tripodsan) for general code debugging.
