# PPP

Paul's Preponderating Prepresser (PPP) is a neat little Python utility that ingests a .PDF e-book and "imposes" it onto letter-size pages, so you can print it out. 

I can hear the hippies crying now: "But PAUL! DUUUUDE! Surely we shouldn't be encouraging people to *print books* on *dead trees!* Think of the *treeeees*, *maaaaaan!*

Hear me out, people. Yes, physical books use paper. So does junk mail. So do CVS receipts. So do the reams of corporate marketing materials that no one will ever read. When you actually *need* a book you can annotate, loan, or read without electricity (what's the carbon footprint of that charger? how about the AWS data center?), PPP is the tool for the job. If you're concerned about environmental impact, there are about 22,000 higher-leverage targets than this program. They're called "private jets". When those no longer exist, *then* we can talk about the occasional hand-bound dead-tree book.

BUT I DIGRESS

**Installation Instructions**

PPP is Linux-only. If you want to port it to Windoze, be my guest. It's written in [Python](https://www.python.org) and assumes you're running `bash` for a shell. Get Python installed on yer system, set up and activate a virtual environment, and do yourself a lil' `pip3 install PyPDF2`.

Additionally, ensure the following packages are installed on the system, using your package manager of choice:
* `pdftk`
* `poppler-utils`
* `psutils`
* `ghostscript`
* `cowsay`

Then `git` the repo down into a directory of your choice and add said directory to yer $PATH by whatever method you like. Now you're ready to *PPPartaaaaay!!*

**Quick-Start Guide**

Acquire a .PDF by whatever method brings you joy, but *definitely not* by going on LibGen. Put that sucker in a convenient place, fire up a terminal, punch in `ppp.py`, and away you go. The program will prompt you at various points. If you know what you're doing, you can stop reading now and let 'er rip, but if you find my writing style entertaining and want to better understand what it's doing, you should probably be familiar with a little bit of the publishing process.

**Workflow Explanation**

A traditionally-bound book actually consists of several little books called *signatures*. In order to make a signature (also called a "section" or "gathering"), we could just staple the individual pages together, one after the other, but that would get bulky and the pages would rip out really easily. Instead, we manipulate the pages around in a special way, so that when the whole signature is collated and folded in half, you can turn the pages and they'll be in the right order. This process is called *imposition*. 

If we make our pages 5.5 x 8.5 inches, we can rotate them and put two on each side of a standard letter-size sheet (called "2-up imposition"). We then use some fancy math to figure out the order to put the pages in so they'll be sequential when the signature is folded. You don't have to memorize the order. PPP does it for you!

Basically, what PPP does is:
* take the source .PDF and check it for errors
* shrink or expand the pages to be 5.5 x 8.5 inches
* rotate and rearrange the pages 2-up
* impose everything into signatures
* output the resulting signatures to a new subfolder
* optionally, batch several signatures together for simplified printing

You then take the resulting .PDFs and print them. Make sure you have permission to do this! Commandeering office equipment can be great fun, but it may be against company policy. Use your own judgment. I just write the software. I'm not responsible for what you do with it.

**Example**

I've included a couple handy-dandy half-letter size example files (lipsum-8.pdf and lipsum64.pdf) for you to mess around with. Let's use the latter to demonstrate how PPP works.

First, do the `chmod +x ppp.py` to ensure it's executable. Then invoke it. You should be able to just `ppp.py` and have it work, but you might have to use `python3 ppp.py` . Try it both ways.

lipsum64.pdf is already the correct size, but if it weren't, PPP will resize it for you. *N.B.:* PPP doesn't change the aspect ratio of the pages - it simply shrinks them to fit. You'll probably end up with whitespace at the top and bottom of the pages. If this bugs you, grab a guillotine cutter and trim the excess after printing. You can also fork the code and fix it yourself. (That don't buffront me, long as I get *my* money next Friday.)

Next, you'll be presented with some choices for how big to make the signatures. Pick whichever one seems best. PPP will preferentially suggest 32- and 36-page signatures. This is about the biggest you can get and still be able to fold cleanly. (By the way, get yourself a bone folder if you're going to be doing a lot of these. There really is no substitute for this specialized tool.)

Next, PPP will split the file into signatures of the correct size. You can bail out here if you want, but 99.9% of the time you'll want to just hit Enter.

Next, PPP will rotate and rearrange the pages, imposing them 2-up. Then it will give you the option to combine several signatures into print jobs, if that's appropriate. (*N.B.:* PPP puts blank sheets between the signatures to make them easier to identify. Pick them out after printing and either put 'em back in the tray or use them for scrap. Your choice.)

At this point you have to take over, because the various PDF readers and printers have different UI. To print the jobs correctly, you'll want to select double-sided, flip SHORT edge.

And that's it!

**Standalone Tools**

If you don't need to run the whole workflow, you can invoke the components separately. `ppp-pad.py` adds blank pages so the signatures divide correctly. `printydump.py` splits the file into signatures. `singledingle` (a `bash` script) imposes a single signature 2-up. `fppp` (another `bash` script) is a wrapper that runs `singledingle` on all the files in a directory.

**Troubleshooting**

Most of the errors I run into involve errant blank pages getting inserted into signatures. If you see asterisks in the imposition output (like this):

```
 ... rearranging pages ...
[*] [1] [2] [*] [*] [3] [4] [41] [40] [5] [6] [39] [38] [7] [8] [37] [36] [9] 
[10] [35] [34] [11] [12] [33] [32] [13] [14] [31] [30] [15] [16] [29] [28] 
[17] [18] [27] [26] [19] [20] [25] [24] [21] [22] [23] 
Wrote 44 pages, 1374472 bytes
 ... imposing pages 2-up ...
[1] [2] [3] [4] [5] [6] [7] [8] [9] [10] [11] [12] [13] [14] [15] [16] [17] 
[18] [19] [20] [21] [22] Wrote 22 pages, 1390639 bytes
 ... re.PDFenating ...
```

... something's gone wrong. Bail out and examine the source file. Chances are, its length isn't a multiple of 4. If there are extra blank pages, strip them out with `pdftk foo.pdf cat x-y output fixed.pdf` or something similar. If you need to add blank pages, those are included. Add them with `pdftk foo.pdf 3pp.pdf cat output fixed.pdf` or something similar.

**Contact**

If you like this software, if you think I'm cool, or otherwise want to get in touch, email [info@neroots.net](mailto:info@neroots.net). If you hate this software or don't think I'm cool, those communications can be routed to `/dev/null`. I'll be sure to check that mailbox periodically.

Yours in Cthulhu,
Paul Fusco-Gessick
Head Honcho, Atlantean Consulting
