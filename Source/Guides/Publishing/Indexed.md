---
layout : Default
---

# Indexed

Publishing your addon to the Index.


## Use Cases

This approach is the easiest way for new users to discover your addon, but it comes with expectations, guidelines and standards.


## Expectations

-   You are expected to maintain your addon for as long as it's indexed. *If it falls into disrepair and is not updated, it may be removed from the index.*

-   Your addon meets the required [Qualities] upon being indexed and works with the Addons team to stay compliant with future changes.


## Recommendations

-   You should ask a small set of users to test your addon before submission (consider reaching out on the [Discord], [Forum], [Reddit]), so people try it out and you receive real usage feedback and can catch important bugs before "going live" to a larger audience.

-   You should tag your repository with at least the `freecad` & `addon` topics to improve searchability.


## Steps

0.  Ensure your addon's code is in a publicly accessible repository.

0.  Ensure your addon meets the required [Qualities] as far as you know how to on your own (assistance is available to meet those you aren't familiar with, so if you are unsure, request a review and the team will help you out).

0.  Ensure basic functionality is in working order before requesting the review. Proof-of-concept and Work-in-Progress Addons are welcome, but should be clearly marked as such, and at least some minimum functionality should exist prior to being added to the Index.

0.  Once you've verified the above, to actually add your addon to the Index, you have three options:

    0.  Open an issue on the GitHub [Addon Index], selecting `Addon - Addition` as the type of Issue.

    0.  Open an issue on the Codeberg [Addon Index Mirror], selecting `Addon - Addition` as the type of Issue.

    0.  Post on the [Addons Subforum] with your request.


## Review

In the review process your addon will be checked to make sure it has the required [Qualities], and the team will work with you to ensure your addon meets the minimum requirements before adding it.

Once it's in compliance you will be asked to make a new release / tag, after which your addon is added to the Index and after a day or so the addition should be reflected in the addon manager.


<!----------------------------------------------------------------------------->

[Qualities]: ../../Topics/Addon-Index/Index/Qualities.md

[Discord]: https://discord.gg/w2cTKGzccC
[Reddit]: https://www.reddit.com/r/freecad
[Forum]: https://forum.freecad.org/

[Addon Index]: https://github.com/FreeCAD/Addons/issues/new/choose
[Addon Index Mirror]: https://codeberg.org/FreeCAD/Addons/issues/new/choose
[Addons Subforum]: https://forum.freecad.org/viewforum.php?f=65