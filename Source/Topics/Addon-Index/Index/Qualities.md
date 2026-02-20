---
layout : Default
---

# Qualities

The following are the desired qualities used for the [Coverage].

<br/>

>   [!NOTE]  
>   Addons that have been registered before the change  
>   to the new Index are afforded time to get up to snuff.  
>
>   They will be reviewed one by one and given support  
>   by the Addon Ecosystem Coordinator where possible.

<br/>

## Thresholds

### 🔵 Low Threshold

Covering all of the qualities marked with 🔵 
is a requirement for any `Indexed` addon.

### 🔴 High Threshold

Covering all of the qualities marked with 🔴 
is a requirement for any `Curated` addon.

<br/>

## Governance

-   🔵 The addon has at least one active maintainer 
    or is in the process of finding a new maintainer.

-   🔵 The addon addresses user concerns such as 
    open issues, pull request, .. in a timely manner.

-   🔴 The addon provides tags & releases for every 
    released version if the host platform supports it.

<br/>

## Compliance

-   🔵 The addon complies with GDPR, doesn't send user 
    data to 3rd parties unless expressly permitted by the 
    user and in the event keeps the data to a minimum.

-   🔵 The addon is open, clear and direct to the user 
    about any external connections, services, etc. it uses, 
    what data it sends, when and how often it does so, etc.

-   🔵 The addon informs its users and re-request consent 
    in the event any of the above mentioned things change.

-   🔵 The addon makes an effort to use secure storage 
    options of the users system if it saves relevant data.

-   🔵 The addon accepts and addresses security reports 
    as soon as possible and implements necessary fixes in 
    a timely manner - including previously released versions.

-   🔵 The addon informs users about security issues as 
    soon as is appropriate and if needed provides adequate 
    instructions on how to resolve the problem locally.

<br/>

### Licensing

-   🔵 The addon has one or more fitting licenses 
    and provides a copy of their text in the source.

-   🔵 The addon makes an effort to add SPDX 
    annotations for license identifiers and part-of 
    file notices to any source files where possible.

    ```Python
    # SPDX-License-Identifier: LGPL-2.1-or-later
    # SPDX-FileNotice: Part of the XYZ addon.
    ```

-   🔴 The addon's source is fully licensenable 
    under an appropriate [OSI Approved License][OSI].

<br/>

### Assets

-   🔴 The addon provides scalable icons.

<br/>

### Code

-   🔵 The addon's code is Python 3+ based.

-   🔵 The addon's code is Qt6+ based.

-   🔵 The addon has a valid manifest 
    with as much information as possible. 

-   🔵 The addon use FreeCAD's module structure.

-   🔵 The addon's source is publicly available.

-   🔵 The addon is compatible with the latest 
    version of FreeCAD unless it's specifically 
    designed to only be used with older versions.

-   🔵 The addon attempts to integrate into the 
    existing facilities of FreeCAD over adding new 
    workbenches when appropriate.

-   🔵 The addon doesn't require dependencies 
    unless they are functionally necessary.

-   🔴 The addon provides support for and accepts 
    translations for any relevant user facing strings.

<br/>

## Future Qualities

The following qualities will be introduced at a later point.

-   Addons use the FreeCAD API package.

    *One of the longer term projects is the creation of* 
    *an official FreeCAD API package that wraps the* 
    *native API to provide a properly versioned interface.*

<br/>

<!----------------------------------------------------------------------------->

[Coverage]: ./Coverage

<!----------------------------------------------------------------------------->

[OSI]: https://opensource.org/licenses