# One series, one link

The website is a static comic library. It needs no server, database, API key or paid hosting. The Publish validated comic website GitHub Actions workflow validates every chapter, packages only public assets and deploys main to GitHub Pages, keeping the same URL for future chapters. Failed checks prevent deployment.

## Register a finished chapter

1. Finish all numbered page masters and the PDF in the private production project.
2. Review art, lettering, continuity and page count. Record a completion report:

```json
{"status":"PASS","storyPages":35,"masterHashes":{"1":"SHA256_OF_PAGE_1","2":"SHA256_OF_PAGE_2"}}
```

Include every page number and its actual SHA256. The importer rejects missing, duplicate, unreviewed or changed pages.

3. From this repository, run:

```text
python tools/publish_chapter.py ../../output/chapter5/pages --chapter 5 --title "Approved chapter title" --review-json ../../production/chapter5-review.json --expected-pages 35 --pdf ../../output/chapter5/Chapter_5.pdf
python tools/validate_library.py
```

The importer preserves the original master proportions, creates reader derivatives, adds the chapter to chapters/chapters.json, rebuilds assets/comic.js and the templates, and checks all chapter images. It refuses to replace any existing chapter. Chapters 1-3 remain byte-for-byte unchanged.

4. Preview with `python -m http.server 8765 --bind 127.0.0.1`. Check desktop/mobile, chapter switching, the new chapter's first and last pages, and Continue Reading. Commit only the reviewed changes and push to main. GitHub Pages updates the existing URL. For a subsequent chapter on an already integrated main branch, `--publish` performs the checked chapter commit and push automatically; use it only after browser QA.

5. Wait for the corresponding successful `pages build and deployment` run, and check the live catalog and chapter images. The Validate complete comic library workflow also checks all approved image hashes on pushes and pull requests. The deployment workflow repeats validation before publishing, so incomplete or changed artwork cannot replace the live version.

## Data and privacy

Only finished comic artwork, reader assets, chapter metadata and publishing code belong here. Production plot notes, character references, rejected images and credentials stay outside the repository. The production project retains lossless PNG masters. The web reader uses full-resolution JPEG derivatives and lazy loading. Continue Reading uses localStorage on the reader's device; it sends no reading history to a server.

## Existing links

All legacy `read.html#3/1` links continue to work. Chapter-one shortcuts such as `read.html#12` also work. No redirect or new per-chapter website is required.
