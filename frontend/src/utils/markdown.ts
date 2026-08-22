import MarkdownIt from "markdown-it";
import hljs from "highlight.js";

// function highlightCode(str: string, lang: string): string {
//   if (lang && hljs.getLanguage(lang)) {
//     return hljs.highlight(str, {
//       language: lang,
//     }).value
//   }

//   return str
// }


const md = new MarkdownIt({
  html: true,
  breaks: true,
  linkify: true,

  highlight(str: string, lang: string): string {
    if (lang && hljs.getLanguage(lang)) {
      return hljs.highlight(str, {
        language: lang,
      }).value
    }

    return ''
  },
})

export default md


