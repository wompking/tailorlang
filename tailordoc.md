###DEFINITIONS###

| Command         | Format |
|-----------------|----------------------------------------------|
| (class)         | type <name> = [string array] or type + type |
| (input)         | gather |
| (evaluate)      | hem <fabric index> |
| (bool)          | condition = <fabric index> <flags> <regex> or <bool> <bool operation> <bool> or not <bool> |
|                 | if/while <bool> { |
|                 |     ...content... |
|                 | } |
| (label)         | notch |
|                 | dye <fabric> <color index> |
| (goto)          | see <line number/notch index> |
| (write)         | embroider <fabric index (not "materials")> <flags> <string> OR embroider <fabric index> <string> |
|                 | copy <fabric index (not "garment")> <flags> <regex> <fabric index (not "materials")> OR copy <fabric index> <fabric index> |
| (modify)        | alter <fabric index (not "materials")> <flags> <regex> <replace> |
| (transliterate) | replace <fabric index (not "materials")> <flags> <type> <type> OR replace <fabric index> <type> <type> |
| (function)      | procedure <name> (<fabric arguments>) { |
|                 |    ...content... |
|                 | } |
| (output)        | sell |
| (halt)          | stop |
| (exit)          | end |
| (call)          | do <procedure name> (<fabric indexes>) |

| Command         | Format |
|-----------------|----------------------------------------------|
| (function)      | procedure <name> (<fabric arguments>) { |
|                 |    ...content... |
|                 | } |
| (call)          | do <procedure name> (<fabric indexes>) |

###FLAGS###

-p : prepend string instead of overwriting match
-a : append string instead of overwriting match

###EXAMPLES###

```
function reverse (fabric){
    bool check = fabric -g /^[?]+.?$/ update
    bool invcheck = not check update
    while invcheck {
        modify fabric -gp /^./ ">"
        modify fabric -g /(>.)(.+[?]?)(.+)/ "$2$1?$3"
        modify fabric - /[>]/ "?"
    }
    modify fabric -g /[?]/ ""
}
```

#Foobar should return rabooF
#Feel free to replace "?" and ">" later so strings with "?" and ">" don't screw up the function

```
function shunt (buffer1, buffer2) {
    copy buffer1 -p /./ buffer2
    modify buffer1 - /./ ""
}

function reverse (buffer){
    bool some = buffer - /./ update
    while some {
        call shunt(buffer, revbuff)
    }
    copy revbuff - // buffer
}
```

#Foobar should return rabooF
#Requires two buffers, but "revbuff" is removed after function execution

```
function add (buffer1, buffer2) {
    bool some_one = buffer1 - /./ update
    bool some_two = buffer2 - /./ update
    bool both = some_one and some_two update
    while both {
         call shunt(buffer1, addbuff)
         call shunt(buffer2, addbuff)
         modify addbuff -p // ";"
    }
    while some_one {
        call shunt(buffer1, addbuff)
        modify addbuff -p // ";0"
    }
    while some_two {
        call shunt(buffer2, addbuff)
        modify addbuff -p // ";0"
    }
    class inc11 = [";0",";1",";2",";3",";4",";5",";6",";7",";8",";9"]
    class inc12 = [";",";0|",";1|",";2|",";3|",";4|",";5|",";6|",";7|",";8|"]
    class inc21 = ["|0","|1","|2","|3","|4","|5","|6","|7","|8","|9","|A","|B","|C","|D","|E","|F","|G","|H"]
    class inc31 = ["|;0","|;1","|;2","|;3","|;4","|;5","|;6","|;7","|;8","|;9"]
    class inc41 = ["0|","1|","2|","3|","4|","5|","6|","7|","8|","9|","A|","B|","C|","D|","E|","F|","G|","H|","I|"
    class over10 = ["A","B","C","D","E","F","G","H","I","J"]
    class base19 = ["1", "2", "3", "4", "5", "6", "7", "8", "9"] + over10
    bool check1 = addbuff -g /^;[0-9]{2}$/ update
    bool check2 = addbuff -g /[A-I]/ update 
    while check1 {
        transliterate addbuff -g inc11 inc12
        transliterate addbuff -g inc21 base19
    while check2 {
        transliterate addbuff -g over10 inc31
        transliterate addbuff -g inc41 base19
        modify addbuff -g /[|]/ "1"
        modify addbuff -p /^[0-9]/ ";"
        modify addbuff -g /;;/ ";0;"
    }
    modify addbuff -g /;/ ""
    call reverse(addbuff)
    copy addbuff - // buffer1
}
```
