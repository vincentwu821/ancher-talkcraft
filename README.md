# Ancher TalkCraft

**Learn how great creators tell stories. Turn your own ideas into talking-head videos.**

Ancher TalkCraft is an Agent Skill that helps you learn narrative structures from videos, podcasts, articles, and posts, then use those structures to express your own ideas on camera. It covers the journey from a reference and a one-sentence idea to a script, recorded footage, an edited video, and social publishing assets.

## Install directly inside Claude Code

Run these two commands in a Claude Code conversation:

```text
/plugin marketplace add vincentwu821/ancher-talkcraft
/plugin install ancher-talkcraft@ancher
```

Choose **Install for you** in the plugin panel. You can also open `/plugin`, go to **Discover**, and search for `ancher-talkcraft` after adding the Ancher marketplace. Claude Code downloads and installs the plugin for you; you do not need to visit GitHub or download a ZIP manually.

Once installed, ask Claude Code to use Ancher TalkCraft. The bundled skill can also be invoked as `/ancher-talkcraft:ancher-talkcraft`. The scripting stage requires connecting your own Ancher account; the skill guides you through that setup when needed.

This is the publisher-maintained **Ancher marketplace**, not an approved listing in Anthropic's default `claude-plugins-official` marketplace. An official directory submission and its review are separate.

## Find and install on skills.sh

[View Ancher TalkCraft on skills.sh](https://skills.sh/vincentwu821/ancher-talkcraft/ancher-talkcraft).

With Node.js and npm available, run:

```sh
npx skills add vincentwu821/ancher-talkcraft --skill ancher-talkcraft
```

Choose your host agent when prompted. You can also give the GitHub repository URL to your agent and ask it to install the skill. A skills.sh listing is independent of the built-in Codex, ChatGPT, and WorkBuddy directories.

## Download

- [WorkBuddy package (.zip)](https://github.com/vincentwu821/ancher-talkcraft/releases/download/v1.1.1/ancher-talkcraft-v1.1.1.zip)
- [Codex / Claude Code package (.zip)](https://github.com/vincentwu821/ancher-talkcraft/releases/download/v1.1.1/ancher-talkcraft-v1.1.1.zip)
- [Doubao Work package (.zip)](https://github.com/vincentwu821/ancher-talkcraft/releases/download/v1.1.1/ancher-talkcraft-doubao-v1.1.1.zip)
- [All releases](https://github.com/vincentwu821/ancher-talkcraft/releases)

**WorkBuddy, Codex, and Claude Code use the same ZIP package.** Follow the separate installation instructions for your app below; their import methods, installation folders, and invocation commands differ. The Doubao Work ZIP uses a lowercase `skill.md` entry point.

The ZIP contains one complete skill folder. After extraction, its structure is:

```text
ancher-talkcraft/
├── SKILL.md
├── references/
├── scripts/
├── assets/
└── ...
```

Keep the folder and its supporting files together. Do not upload only `SKILL.md`, add an extra wrapper directory, or include a `.git` directory.

## What it does

1. **Learn from a reference.** Save inspiring content to [Ancher](https://ancher.ai), let it finish processing, and analyze its hook, argument, examples, transitions, pacing, and ending.
2. **Make the story your own.** Describe what you want to say in one or two sentences. Ancher's own Agent combines your input with the reference analysis to create a script. All script revisions go back to that same Agent.
3. **Record yourself.** Use your preferred camera or recording app. An optional illustrated Douyin teleprompter guide is included.
4. **Produce the video.** Your host agent edits your actual footage, removes repetition, adjusts pacing naturally, smooths the voice, and creates word-by-word animated captions with a fixed top headline.
5. **Finish and publish.** Review a music-free rough cut first, audition licensed background music, and get face-forward covers and platform-specific copy. Each revision is saved separately.

Already have footage? Start directly with editing; that branch does not require Ancher.

## Install

### Codex

Download the **Codex / Claude Code package (.zip)** above and extract it so the complete folder is located at:

```text
~/.agents/skills/ancher-talkcraft/SKILL.md
```

Keep `references/`, `scripts/`, `assets/`, and the other included files alongside it. Start a new session and invoke `$ancher-talkcraft`.

### Claude Code

Use the [in-app marketplace installation](#install-directly-inside-claude-code) above. If you prefer a standalone skill instead of the plugin, extract the ZIP folder into:

```text
~/.claude/skills/ancher-talkcraft/SKILL.md
```

For this standalone installation, invoke `/ancher-talkcraft`. A project-level `.claude/skills/` directory can also be used. Choose one installation method so you do not load duplicate copies.

### WorkBuddy

Open the Skills section, choose **Add skill > Upload skill**, and upload the **WorkBuddy package (.zip)** above. Keep the `.zip` extension; do not rename it to `.skill`. WorkBuddy handles unpacking the uploaded package. If your import interface offers a folder picker, select the complete extracted `ancher-talkcraft` folder shown above. Confirm that the imported skill is enabled. Importing for your own use does not publish the skill to the public marketplace.

### Doubao Work

Use the dedicated Doubao Work ZIP in its custom skill import interface. The regular Doubao chat interface may not provide the MCP or local media execution tools needed for the complete workflow.

## Try it

```text
Use ancher-talkcraft. I like how this creator explains a complicated idea.
Here is the reference: [link or attachment].
My topic is: [one sentence about your own idea].
First check whether Ancher is connected.
```

Or start from footage:

```text
Use ancher-talkcraft to edit these recorded clips into a clear, lively
talking-head video. Keep the later takes where they are better, add
word-by-word animated captions and a fixed top headline, and show me
a rough cut without music first.
```

## Requirements and boundaries

- **Scripting:** An Ancher account, an authorized Ancher MCP connection, and access to Ancher's own Agent. If the connection is missing, the skill helps you set it up. The host model must not substitute its own script or call a model provider directly instead.
- **Production:** A host with access to your media files and suitable editing, transcription, word alignment, image, and rendering tools. Capabilities vary across clients; importing the skill alone does not install these tools.
- **Language:** The public overview and skill description are in English. The detailed workflow and reference guides are currently in Chinese, with Chinese-language talking-head content as their default use case.
- **Platform support:** Installation conventions are documented; the full video workflow has not been tested end to end in every supported client.

See [the full workflow](SKILL.md) and [installation and capability details](references/install.md).

## Privacy and optional registration

Email registration is **disabled by default**. The distributed configuration contains no collector endpoint, credentials, or recipient identity. It does not collect or send email addresses unless a publisher explicitly configures registration and a user gives informed consent.

Keep recordings, generated scripts, account tokens, and registration receipts in your own project or local state directories, outside the distributable skill folder. See [publisher setup](references/publisher-setup.md) before enabling registration.

## License

The original skill instructions, code, and documentation are licensed under the [MIT License](LICENSE). Third-party tutorial images and their embedded content are excluded from that grant and remain subject to their respective owners’ rights.

## Third-party tutorial material

The optional recording guide includes attributed excerpts from a third-party tutorial. Attribution and the original source are in [assets/shooting/SOURCE.txt](assets/shooting/SOURCE.txt). Rights to those excerpts remain with their respective owners; no independent license to those materials is granted here.
