# Variables usage

## Declaring a variable

You can set a value using the `set` function. 
> set `config.url` http://localhost:8080

## Reusing a variable

If you would like to reuse previously set variable you can do it like below:

> set `config.new_url` {{ config.url }}

## Declaring a complex variable with a block-code

To set complex value like an array or object use json or yaml code block:

> set `config.address`

```yaml
street_name: Seasame street
post_code: ABC 123
city: New York
```

## Printing a variable

To print set variables use `print` function

> print config

You can also dump variables to a file by using print function

> print config > ./variables.yml


# Using modifiers/filters
Before variable goes to output it can be piped into filters/modifiers to
customize its value.

## Transforming to upper-case

> print {{ string | uppercase }}

## Transforming to lower-case

> print {{ string | lowercase }}

## Transforming to snake-case

> print {{ string | snakecase }}

## Stripping whitespace

> print {{ string | strip }}

# Built-in functions

## Setting new uuid

> set my_uuid {{ uuid() }}

## Setting new object-id

> set my_objectid {{ objectid() }}

## Setting current date

> set my_date {{ date() }}

## Setting current date-time

> set my_time {{ datetime() }}

## Setting current time

> set my_time {{ time() }}
