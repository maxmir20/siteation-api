<img width="128" height="128" alt="icon_128" src="https://github.com/user-attachments/assets/f060d94f-e765-4440-80e0-9ae314f39a78" />

# Site-ation

## What if you could use crowd-sourcing to see how often an online resource helped someone with a coding problem?
### That's the idea behind Site-ation, an open-source collaborative database that lets developers credit the resources (e.g. webpages/articles/blogs/StackOverflow posts/etc) that helped them write their PR. 

Site-d pages appear publicly for other users, allowing you to get a sense if a page has helped others before

With Site-ation installed you can:
1. See whether the website has been Site-d by any users <img width="29" height="24" alt="Screenshot 2025-10-16 at 2 55 50 PM" src="https://github.com/user-attachments/assets/c1733181-3eda-4fe1-b1a3-3ae0d85788cb" />
2. See how often the page you're on has been Site-d by other users <img width="23" height="24" alt="Screenshot 2025-10-16 at 2 55 37 PM" src="https://github.com/user-attachments/assets/4557cece-11d5-4a9e-a1d8-612027e62a04" />

3. Contribute Site-ations by including them in your PRs
<img width="600" height="268" alt="Screenshot 2025-10-16 at 3 26 07 PM" src="https://github.com/user-attachments/assets/e0a89016-c75c-4dda-a13d-4fa89037386c" />


## Technical implementation
Site-ation is a Browser Extension and GitHub Action that uses DynamoDB to store URLs

<img width="820" height="341" alt="Screenshot 2025-09-14 at 7 10 30 PM" src="https://github.com/user-attachments/assets/739fe0ff-44b4-47f4-a18a-89cdc892aafb" />


Site-ation aims to access as little information from your Org/Repo as possible. **No information or contents about your Identity, PR, Account, or Org are accessed or stored except for any URLs that are located under a "[Site-ations]" list in your initial PR's Issue Description section**.

<img width="492" height="571" alt="Screenshot 2025-10-16 at 3 16 05 PM" src="https://github.com/user-attachments/assets/b40a7dd9-f5b8-43a6-8d5a-34e42fffa7ae" />


## Installation Instruction:
### Github App
#### 1. Go to the [Site-ation Github App](https://github.com/apps/site-ation) and add it to your user account:
<kbd>
  <img width="1079" height="438" alt="Screenshot 2025-09-14 at 2 16 39 PM" src="https://github.com/user-attachments/assets/53b87250-57cb-434c-9da9-92df996af918" />
</kbd>

#### 2. Click "Configure"

#### 3. Add it to the selected repositories you would like it to be active on:
<kbd>
  <img width="958" height="695" alt="Screenshot 2025-09-14 at 2 16 10 PM" src="https://github.com/user-attachments/assets/feb5ffdc-f365-4c12-a2c7-99f22a19f468" />
</kbd>


### Browser Extension:
From the Chrome Browser Extension Marketplace, install the Site-ation Extension: https://chromewebstore.google.com/detail/nbflhjdhpokppngahofkpjgoamnnoffe?utm_source=item-share-cb

Github Repo for Browser Extension: https://github.com/maxmir20/siteation-extension

### Usage:
#### Viewing Site-ations:
While navigating around the web, if a site has any site-ations, then the extension Icon will turn Green. If you land on a specific page that has been cited, the page's site-ation score will appear next to the extension icon.

[Loom Video Demo - Viewing Site-ations](https://www.loom.com/share/7c5f427c92fe4559a9cddc7f56300e76?sid=4622ccbf-466e-44a7-a679-e0c1634d21a1) 

#### Adding Site-ations:
If you see a link you would like to save for your PR, click the Site-ation icon once to add the link to your list of Site-ations.
Once you are on your github PR page, double-click the icon to copy all your Site-ations onto your clipboard. Site-ations will be autoformatted to allow for easy pasting. 

_Note: All currently stored Site-ations are deleted once you copy them to the clipboard_

After listing your Site-ations in your PR description, the site-ations will be added **_once you merge your PR_**.

[Loom Video Demonstration - Adding Site-ations](https://www.loom.com/share/3365ee925f134b249249fde9e1031c56?sid=460e06c3-7d57-4a54-9b1f-bda5aa032c40)
