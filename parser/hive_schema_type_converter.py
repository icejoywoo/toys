#!/usr/bin/env python2.7
# encoding: utf-8

"""
    @brief: 一个类型转换为自定义类型 json 的脚本，支持类型的嵌套

    例如：string 变为 {"metadata":{"chineseName":null,"desc":null},"name":"simple_string","nullable":true,"type":"string"}
    @author: icejoywoo
    @date: 2018/8/27
"""

type_mapping = {
    'string': 'string',
    'bigint': 'long',
    'int': 'integer',
    'smallint': 'integer',
    'tinyint': 'integer',
    'short': 'integer',
    'float': 'float',
    'double': 'double',
}


def basic_type(t):
    return type_mapping.get(t, t)


def array_type(element_type):
    return {
        "type": "array",
        "containsNull": True,
        "elementType": get_type(element_type),
    }


def map_type(key_type, value_type):
    return {
        "type": "map",
        "keyType": basic_type(key_type),
        "valueType": get_type(value_type),
        "valueContainsNull": True,
    }


def struct_type(type_string, delimiter=':', seperator=','):
    # 可能出现的两种括号

    brackets = {
        '<': '>',
        '[': ']',
        '(': ')',
        '{': '}',
    }

    def match_bracket(prev, last):
        return brackets[prev] == last

    bracket_stack = []

    special_chars = brackets.keys() + brackets.values() + [delimiter, seperator]

    item_start = 0
    key = None
    value = None

    # 是否在括号内
    in_bracket = False

    fields = []

    for i, c in enumerate(type_string + seperator):
        if c in special_chars:
            if c in brackets.keys():
                bracket_stack.append(c)
                in_bracket = True
            elif in_bracket and c in brackets.values():
                if bracket_stack and match_bracket(bracket_stack.pop(), c):
                    in_bracket = False
                else:
                    # 并非严格匹配括号，只检查有括号前缀的情况
                    raise ValueError("bracket doest not match")
            elif c == delimiter and not in_bracket:
                key = type_string[item_start:i]
                item_start = i + 1
            elif c == seperator and not in_bracket:
                value = type_string[item_start:i]
                item_start = i + 1
                if key:
                    fields.append({
                        "name": key,
                        "type": get_type(value),
                        "nullable": True,
                    })
                key = None
                value = None

    return {
        "type": "struct",
        "fields": fields,
    }


def get_type(_type):
    if _type in type_mapping.keys():
        return basic_type(_type)
    elif _type.startswith("array"):
        inner_type = _type[6:-1]
        return array_type(inner_type)
    elif _type.startswith("map"):
        types = _type[4:-1]
        key_type, value_type = [i.strip() for i in types.split(",", 1)]
        return map_type(key_type, value_type)
    elif _type.startswith("struct"):
        types = _type[7:-1]
        return struct_type(types)
    else:
        raise ValueError("UnknownType[%s]" % _type)


def full_type(name, _type, desc=None, comment=None):
    return {
        "name": name,
        "type": get_type(_type),
        "nullable": True,
        "metadata": {
            "desc": desc,
            "chineseName": comment,
        }
    }


def parse_table_schema(table_schema):

    fields = []
    for column_schema in table_schema:
        fields.append(full_type(*column_schema))

    schema = {
        "type": "struct",
        "fields": fields
    }

    return schema


def eq(expected, name, _type):
    import json
    result = json.dumps(full_type(name, _type), sort_keys=True, indent=2)
    assert expected == result


if __name__ == '__main__':
    eq("""{
  "metadata": {
    "chineseName": null, 
    "desc": null
  }, 
  "name": "simple_string", 
  "nullable": true, 
  "type": "string"
}""", "simple_string", "string")

    eq("""{
  "metadata": {
    "chineseName": null, 
    "desc": null
  }, 
  "name": "string_array", 
  "nullable": true, 
  "type": {
    "containsNull": true, 
    "elementType": "string", 
    "type": "array"
  }
}""", "string_array", "array<string>")

    eq("""{
  "metadata": {
    "chineseName": null, 
    "desc": null
  }, 
  "name": "string_map", 
  "nullable": true, 
  "type": {
    "keyType": "string", 
    "type": "map", 
    "valueContainsNull": true, 
    "valueType": "string"
  }
}""", "string_map", "map<string, string>")

    eq("""{
  "metadata": {
    "chineseName": null, 
    "desc": null
  }, 
  "name": "string_map_array", 
  "nullable": true, 
  "type": {
    "containsNull": true, 
    "elementType": {
      "keyType": "string", 
      "type": "map", 
      "valueContainsNull": true, 
      "valueType": "string"
    }, 
    "type": "array"
  }
}""", "string_map_array", "array<map<string, string>>")

    eq("""{
  "metadata": {
    "chineseName": null, 
    "desc": null
  }, 
  "name": "nested_map", 
  "nullable": true, 
  "type": {
    "keyType": "string", 
    "type": "map", 
    "valueContainsNull": true, 
    "valueType": {
      "keyType": "integer", 
      "type": "map", 
      "valueContainsNull": true, 
      "valueType": "integer"
    }
  }
}""", "nested_map", "map<string, map<int, int>>")

    eq("""{
  "metadata": {
    "chineseName": null, 
    "desc": null
  }, 
  "name": "struct_array", 
  "nullable": true, 
  "type": {
    "containsNull": true, 
    "elementType": {
      "fields": [
        {
          "name": "id", 
          "nullable": true, 
          "type": "string"
        }, 
        {
          "name": "map", 
          "nullable": true, 
          "type": {
            "keyType": "string", 
            "type": "map", 
            "valueContainsNull": true, 
            "valueType": "integer"
          }
        }, 
        {
          "name": "num_1", 
          "nullable": true, 
          "type": "integer"
        }, 
        {
          "name": "num_2", 
          "nullable": true, 
          "type": "integer"
        }
      ], 
      "type": "struct"
    }, 
    "type": "array"
  }
}""",
    "struct_array", "array<struct<id:string,map:map<string,int>,num_1:int,num_2:int>>")
