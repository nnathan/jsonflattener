# JSON Flattener

This software is public domain.

## Usage

### Basic Example

```
python fj.py <<EOF
[
  {
    "hello": 5,
    "zap": {
      "limb": {"thing": 10},
      "blast": [{"terminal": 5}, 13, null]
    },
    "nothing": null
  }
]
EOF
```

Outputs:

```
[0].nothing: null
[0].hello: 5
[0].zap.blast.[1]: 13
[0].zap.blast.[2]: null
[0].zap.blast.[0].terminal: 5
[0].zap.limb.thing: 10
```

### Advanced Example

```
# note: if you want to use '=' instead of 🍺  you will want to do: -v==
python3 fj.py -l '{' -r '}' -n -p '>' -v🍺 <<EOF
{
  "hello": 5,
  "zap": {
    "limb": {"thing": 10},
    "blast": [{"terminal": 5}, 13, null]
  },
  "nothing": null
}
EOF
```

Outputs:

```
hello🍺5
nothing🍺
zap>blast>{1}🍺13
zap>blast>{2}🍺
zap>blast>{0}>terminal🍺5
zap>limb>thing🍺10
```
