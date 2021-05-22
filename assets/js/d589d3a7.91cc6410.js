(self.webpackChunkwebsite=self.webpackChunkwebsite||[]).push([[162],{601:function(e,t,n){"use strict";n.r(t),n.d(t,{frontMatter:function(){return o},metadata:function(){return l},toc:function(){return s},default:function(){return p}});var a=n(2122),i=n(9756),r=(n(7294),n(3905)),o={},l={unversionedId:"getting-started",id:"getting-started",isDocsHomePage:!1,title:"Getting started",description:"Installation",source:"@site/docs/getting-started.md",sourceDirName:".",slug:"/getting-started",permalink:"/dispair/docs/getting-started",editUrl:"https://github.com/GDWR/dispair/edit/main/docs/docs/getting-started.md",version:"current",frontMatter:{},sidebar:"tutorialSidebar"},s=[{value:"Installation",id:"installation",children:[]},{value:"QuickStart",id:"quickstart",children:[]}],d={toc:s};function p(e){var t=e.components,n=(0,i.Z)(e,["components"]);return(0,r.kt)("wrapper",(0,a.Z)({},d,n,{components:t,mdxType:"MDXLayout"}),(0,r.kt)("h2",{id:"installation"},"Installation"),(0,r.kt)("p",null,(0,r.kt)("em",{parentName:"p"},"Prerequisite: ",(0,r.kt)("a",{parentName:"em",href:"https://www.python.org/"},"Install Python 3.8+")," on your local environment.")),(0,r.kt)("p",null,"Use the package manager ",(0,r.kt)("a",{parentName:"p",href:"https://pip.pypa.io/en/stable/"},"pip")," to install dispair."),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-cmd"},"pip install dispair\n")),(0,r.kt)("h2",{id:"quickstart"},"QuickStart"),(0,r.kt)("pre",null,(0,r.kt)("code",{parentName:"pre",className:"language-python"},'from dispair import Router\nfrom dispair import WebhookClient\n\nrouter = Router()\n\n@router.interaction(name="8ball", description="Let the 8ball take the wheel")\nasync def _8ball(inter: Interaction):\n    answer = random.choice(["Yes", "No", "Maybe"])\n    return f"> {answer}"\n\ndef main() -> None:\n    if os.getenv("ENVIRONMENT") is None:\n        load_dotenv(dotenv_path=\'.env\')\n\n    client = WebhookClient(\n        os.getenv("BOT_TOKEN"),\n        os.getenv("APP_ID"),\n        os.getenv("APP_PUBLIC_KEY"),\n    )\n\n    client.attach_router(router)\n\n    client.run()\n\n\nif __name__ == "__main__":\n    main()\n')),(0,r.kt)("p",null,"In this quickstart example, we:"),(0,r.kt)("ul",null,(0,r.kt)("li",{parentName:"ul"},"Create a ",(0,r.kt)("inlineCode",{parentName:"li"},"dispair.Router")," and create an interaction route"),(0,r.kt)("li",{parentName:"ul"},"Define a ",(0,r.kt)("inlineCode",{parentName:"li"},"dispair.WebhookClient")," and pass in our necessary environment variables: our discord ",(0,r.kt)("inlineCode",{parentName:"li"},"BOT_TOKEN"),",\nour discord ",(0,r.kt)("inlineCode",{parentName:"li"},"APP_ID"),", and our discord ",(0,r.kt)("inlineCode",{parentName:"li"},"APP_PUBLIC_KEY"),", all of which we can find at the\n",(0,r.kt)("a",{parentName:"li",href:"https://discord.com/developers/applications"},"Discord Developer Portal")),(0,r.kt)("li",{parentName:"ul"},"Run our client")))}p.isMDXComponent=!0}}]);