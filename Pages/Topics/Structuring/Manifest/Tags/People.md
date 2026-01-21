
# People

The `<maintainer>` & `<author>` tags  
specify the people working on an addon. 

<br/>

## General

At least one of each should be present in the  
`<package>` tag, however there is no limit to  
how many people can be credited this way.

*» Check the [Manifest] of the [Template] for an example.*

<br/>

## Syntax

Specify the name of the person inside as the tag  
value and optionally add the `email` attribute.

```xml
<maintainer
    email = '‹Email›'
>‹Name›</maintainer>

<author
    email = '‹Email›'
>‹Name›</author>
```

<br/>

## Example

In this example `The Progenitor` was the original author  
of the addon and `The Descendant` took over maintainership.

```xml
<maintainer
    email = 'Descendant@website.com'
>The Descendant</maintainer>

<author
    email = 'Descendant@website.com'
>The Descendant</author>

<author>The Progenitor</author>
```

<br/>


[Manifest]: https://github.com/FreeCAD/Addon-Template/blob/Latest/package.xml
[Template]: https://github.com/FreeCAD/Addon-Template