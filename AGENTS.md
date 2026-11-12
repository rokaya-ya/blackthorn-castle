# Blackthorn Castle website and publishing

This repository belongs only to the Blackthorn Castle comic. Do not operate on Secret Lair or any other game project.

The permanent reader lives at the existing GitHub Pages URL: https://rokaya-ya.github.io/blackthorn-castle/ . Preserve this URL and repository visibility unless the user explicitly approves a change.

Original chapter artwork, dialogue and order are authoritative. Never replace an existing chapter through the importer. Keep production scripts, private plot notes, reference portraits, credentials and browser profiles outside this public repository.

For “Create Chapter N and publish it”: complete illustration, lettering and continuity review first. Keep the PNG masters in the production project. Create a completion JSON with status PASS, storyPages, and masterHashes mapping every one-based page number to its approved master SHA256. Register only the next chapter with tools/publish_chapter.py; it checks the review hashes, exact page count, resolution and existing content before modifying the catalog. Use --pdf when the finished chapter PDF exists. The catalog automatically drives the homepage, order and both directions of chapter navigation.

Run python tools/build_library.py and python tools/validate_library.py. Run browser checks of the changed chapter, reading progress, mobile layout and navigation. Only then commit the finished chapter and publish to the existing repository's main branch. GitHub Pages deploys main automatically. Monitor the matching Pages run until success and verify the live catalog and all new images before reporting publication. If repository write access or deployment fails, retain the completed files and report the actual blocker; never claim the site updated.

Legacy make_pages.py and issue-import workflows remain for historical compatibility. The production workflow is publish_chapter.py with the reviewed-master completion report. New work must satisfy validate_library.py before publishing.
