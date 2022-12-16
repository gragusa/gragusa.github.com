import bibtexparser
from bibtexparser.bparser import BibTexParser

#from scholarly import scholarly
import chevron
import html
import json

def div(str, _class =""):
    op = '\n<div class="'+ _class +'">'
    cl = "</div>\n"
    return op+str+cl
def a(str, _class ="", href=""):
    op = '\n<a class="'+_class+'" href="'+href+'">'
    cl = "</a>"
    return op+str+cl

def scholarlink(scholarid):
    base_url = "https://scholar.google.com/citations?user="
    return base_url+scholarid

def me(): 
    return "G. Ragusa"

""" 
Get all coathors and they google scholar_id and output to 
coauthors_googlescholar.txt

Example:
getscholarid(bib_database.entries)

This is not run everytime as it is espensive. 
If there is a new coauthor do it.
"""
def getscholarid(entries):
    coauthors = []
    for entry in entries:
        for author in entry["author"]:
            if author == "Ragusa, Giuseppe":
                pass
            else:
                coauthors.append(author)    
    coauthors = list(set(coauthors))
    coauthors.sort()

    for coauthor in coauthors:
        search_query = scholarly.search_author(coauthor)
        try:
            first_author_result = next(search_query)    
            d = {"name": coauthor, "scholar_id": first_author_result["scholar_id"]}
            coauthors_googlescholar.append(d)
        except:
            pass

    with open('bibliography/coauthors_googlescholar.txt', 'w') as convert_file:
          convert_file.write(json.dumps(coauthors_googlescholar))


## Parse Bibliography File
# Parser
parser = BibTexParser()
parser.ignore_nonstandard_types = True
parser.homogenize_fields = False
parser.common_strings = True
parser.customization = bibtexparser.customization.author

with open('bibliography/publications.bib') as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file, parser)

## Remove {} from titles
entries = []
for entry in bib_database.entries:
    entry["title"] = entry["title"].replace("{", "")
    entry["title"] = entry["title"].replace("}", "")
    if "publisher" in entry:
        entry["publisher"] = entry["publisher"].replace("{\\&}", "&")
    if "pages" in entry:        
        entry["pages"] = entry["pages"].replace("--", "-")
        entry["pages"] = entry["pages"].replace("–-", "-")

    entries.append(entry)

with open('bibliography/coauthors_googlescholar.txt', 'r') as f:
    lines = f.readlines()    
coauthors_googlescholar = json.loads(lines[0])

# Split by type
articles = list(filter(lambda d: d['type'] in ["article"], bib_database.entries))
incollections = list(filter(lambda d: d['type'] in ["bookchapter"], bib_database.entries))
wp = list(filter(lambda d: d['type'] in ["wp"], bib_database.entries))
pol = list(filter(lambda d: d['type'] in ["policy"], bib_database.entries))
polit = list(filter(lambda d: d['type'] in ["policy-italian"], bib_database.entries))

# Sort list of dictionary by date and type
articles = sorted(articles, key=lambda d: d['year'], reverse=True)
wp = sorted(wp, key=lambda d: d['year'], reverse=True)
incollections = sorted(incollections, key=lambda d: d['year'], reverse=True)
pol = sorted(pol, key=lambda d: d['year'], reverse=True)
polit = sorted(polit, key=lambda d: d['year'], reverse=True)

def dobibliography(entries, mustachefile, biblioname, dorecent=False):
    articles_html = ""
    recent_html = ""
    count = 0
    for entry in entries:        
        authors = ""
        for author in entry["author"]:
            if authors == '':
                pass
            else:
                if author == entry["author"][-1]:
                    authors += " and "
                else:
                    authors += ", "
            ausplit = author.split(",")
            ss = ausplit[1][1:2]+'. '+ausplit[0]
            if ss==me():
                ss = div(me(), _class="me")
            else:
                google_info = list(filter(lambda d: d['name']==author, coauthors_googlescholar))
                if len(google_info) == 1:
                    scholar_url = scholarlink(google_info[0]["scholar_id"])
                else:
                    scholar_url =""   
                ss = a(ss, _class="coauthor", href=html.escape(scholar_url))
            authors += ss

        entry["authors"] = authors

        ## Keep only non empty keys
        entry = {k: v for k, v in entry.items() if v}

        entry["has_doi"] = "doi" in entry
        entry["has_number"] = "number" in entry
        entry["has_volume"] = "volume" in entry
        entry["has_preprint"] = "preprint" in entry
        entry["has_code"] = "code" in entry
        entry["nothas_preprint"] = not "preprint" in entry
        entry["nothas_code"] = not "code" in entry
        entry["has_pages"] = "pages" in entry

        with open("bibliography/"+mustachefile, 'r') as f:
            ah = chevron.render(f, entry)        

        articles_html += ah

        if "recent" in entry and entry["recent"]=="true":
            count += 1        
            recent_html += ah

        if dorecent and count == 2:
            with open('bibliography/recent.txt', 'w') as f:
                f.writelines(recent_html)
            count = 3

    with open(biblioname, 'w') as f:
        f.writelines(articles_html)

## Create articles.txt
dobibliography(articles, "article.mustache", "bibliography/"+"articles.txt", dorecent=True)
dobibliography(incollections, "incollection.mustache", "bibliography/"+"incollections.txt", dorecent=False)
dobibliography(wp, "wp.mustache", "bibliography/"+"wp.txt", dorecent=False)
dobibliography(pol, "pol.mustache", "bibliography/"+"pol.txt", dorecent=False)
dobibliography(polit, "pol.mustache", "bibliography/"+"polit.txt", dorecent=False)


