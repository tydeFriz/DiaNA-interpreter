# DiaNA-interpreter
an interpreter for a not really usable language that works like DNA called DiaNA


## The language
DiaNA is a DNA-inspired language where code is always self-changing and execution can be randomic.

At runtime, the code is separated into "Strands" which are composed of "Acids".

An Acid is a single line of code, composed of an operator and its parameters; a Strand is a sequence of Acids.

Strands are separated by empy lines.

Code is executed by "Runners".

A Runner executes a Strand sequentially, Acid by Acid, then dies when there are no more Acids to execute.

There are 6 operators:
- LABEL
- CUT
- GLUE
- COPY
- KILL
- RUN

Parameters are written after the operator and separated by a single space.
Here are some examples:
```
LABEL a
CUT a UP
GLUE a b
COPY a
KILL a
RUN a
```

### LABEL operator
The LABEL operator acts as a reference for other operators.

It takes a single parameter which is any alfanumeric string that can also contain the '_' character.

There is a special LABEL operator, "LABEL Start", which identifies the Strand that the initial Runner will execute.

A LABEL Start operator is only valid if it it the first Acid of its Strand.

There can be multiple LABEL Start operators in the code, but only one of them (choosen at random at runtime) will act as the starting point.

### CUT operator
The CUT operator separates a Strand into 2 Strands.
It takes 2 parameter:
- the first is a label that it will be searched in the code.
- the second is a string wich is either "UP" or "DOWN".

The CUT operator searches the whole code for LABEL Acids that match its first parameter and takes one at random.

It then separates the Strand into 2 cutting where the Acid is.

The Acid is then either added as a last Acid of the first trand or the first Acid of the second one depending on the second parameter.

A LABEL Acid is not considered valid for the CUT operation if it doesn't have another Acid to separate it from.

CUT exmaple 1:

```
LABEL Start
CUT c UP

LABEL a
LABEL b
LABEL c
```
running this code will result in the following Strands:
```
LABEL Start
CUT c UP

LABEL a
LABEL b

LABEL c
```

CUT example 2:
```
LABEL Start
CUT a DOWN

LABEL a
LABEL b
LABEL c
```
running this code will result in the following Strands:
```
LABEL Start
CUT a DOWN

LABEL a

LABEL b
LABEL c
```

CUT example 3:
```
LABEL Start
CUT a DOWN

LABEL b
LABEL a

LABEL a
LABEL b
```
running this code will result in the following Strands:
```
LABEL Start
CUT a DOWN

LABEL b
LABEL a

LABEL a

LABEL b
```
This will always be the case because the lonely "LABEL a" Acid has nothing to cut below it.


### GLUE operator
The GLUE operator attatches 2 Strands into a single one.

It takes 2 parameter, both being labels.

The GLUE operator searches the whole code for Strands which ending Acid is a LABEL operator matching the first parameter and takes one at random.

It then searches the whole code for Strands which starting Acid is a LABEL operator matching the second parameter and takes one at random.

If 2 valid Strands are found, the second one is appended to the first one.

GLUE example:
```
LABEL Start
GLUE d a

LABEL a
LABEL b

LABEL c
LABEL d
```
running this code will result in the following Strands:
```
LABEL Start
GLUE d a

LABEL c
LABEL d
LABEL a
LABEL b
```

### COPY operator
The COPY operator copies an entire Strand.

It takes a single parameter, being a label.

The COPY operator searches the whole code for Strands which starting Acid is a LABEL operator matching the parameter and takes one at random.

If a valid Strand is found, it creates a new Strand which is an exact copy of the found one.

COPY example:
```
LABEL Start
COPY a

LABEL a
LABEL b
LABEL c

```
running this code will result in the following Strands:
```
LABEL Start
COPY a

LABEL a
LABEL b
LABEL c

LABEL a
LABEL b
LABEL c
```

### KILL operator
The KILL operator deletes an entire Strand.

It takes a single parameter, being a label.

The KILL operator searches the whole code for Strands which starting Acid is a LABEL operator matching the parameter and takes one at random.

If a valid Strand is found, it deletes the Strand entirely.

KILL example:
```
LABEL Start
KILL a

LABEL a
LABEL b
LABEL c

LABEL d
LABEL e
```
running this code will result in the following Strands:
```
LABEL Start
KILL a

LABEL d
LABEL e
```

### RUN operator
The RUN operator creates a Runner that executes a Strand.

It takes a single parameter, being a label.

The KILL operator searches the whole code for Strands which starting Acid is a LABEL operator matching the parameter and takes one at random.

If a valid Strand is found, a Runner is created for that Strand.

The RUN operator can trivially used to make infinite loops:
```
LABEL Start
RUN a

LABEL a
COPY b
RUN a

LABEL b
```
running this code will infinitely create new copies of the Strand containing the LABEL b Acid.

# WIP
