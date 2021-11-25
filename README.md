### OutreachBot
Outreach is an essential part of many businesses, and often times companies have dedicated employees for this job. This bot was created in order to optimize outreach tasks, potentially saving hours of work. The bot takes a list of links to company webpages, scrapes them for their facebook page and then extracts their contact email.

### How to use
Using this tools involves three basic components: the input folder, the code (OutreachBot.py), and the output folder, which can all be found on the folder named "Bot" on the OutreachBot repository.
The first step is adding a csv file containing the links of links to company webpages that you want to use. This csv file should only contain a column of links with any header. Keep in mind that only one file should be in the Input folder, if there is more than one, the bot may take an undesired file as input.
The next step is to run the code in the OutreachBot.py file, either directly from console or using a code editor. Additionally, the repo also includes an "OutreachBot.ipynb" file, in case the user prefers using JupyterNotebook or JupyterLab.
After performing this step, a new csv file will appear on the "Output" folder. This file will now contain the original list of company webpages, as well as two new columns conatining the Facebook link, if found, and the contact email located on the Facebook page, if any. If no Facebook link or contact email are present in their respective webpages that field will simply be empty.
