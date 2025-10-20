import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Separator } from "@/components/ui/separator"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"

function About() {
  return (
    <div className="space-y-10 p-6">
      <Card>
        <CardHeader className="flex items-center gap-4">
          <Avatar className="h-16 w-16">
            <AvatarImage src="https://github.com/shadcn.png" alt="Remote Team" />
            <AvatarFallback>RT</AvatarFallback>
          </Avatar>
          <div>
            <CardTitle className="text-3xl">Remote Experience</CardTitle>
            <CardDescription>
              Building composable micro-frontends with care and precision.
            </CardDescription>
            <div className="mt-2 flex items-center gap-2">
              <Badge variant="default">Micro-frontend</Badge>
              <Badge variant="secondary">TypeScript</Badge>
              <Badge variant="outline">Shadcn UI</Badge>
            </div>
          </div>
        </CardHeader>
        <CardContent className="grid gap-6 md:grid-cols-[1fr_280px]">
          <div className="space-y-6">
            <p className="text-muted-foreground">
              Remote helps you assemble user experiences that feel local—no matter where the code lives.
              We focus on consistency, performance, and developer happiness.
            </p>

            <Tabs defaultValue="mission" className="w-full">
              <TabsList>
                <TabsTrigger value="mission">Mission</TabsTrigger>
                <TabsTrigger value="culture">Culture</TabsTrigger>
                <TabsTrigger value="stack">Stack</TabsTrigger>
              </TabsList>
              <TabsContent value="mission" className="space-y-2">
                <h3 className="text-lg font-semibold">Empower every team</h3>
                <p className="text-muted-foreground">
                  Provide tools and patterns that enable seamless UI integration across distributed teams.
                </p>
              </TabsContent>
              <TabsContent value="culture" className="space-y-2">
                <h3 className="text-lg font-semibold">Async & inclusive</h3>
                <p className="text-muted-foreground">
                  Collaboration is built on clear interfaces, empathetic reviews, and relentless automation.
                </p>
              </TabsContent>
              <TabsContent value="stack" className="space-y-2">
                <h3 className="text-lg font-semibold">Modern tooling</h3>
                <p className="text-muted-foreground">
                  React, TypeScript, Vite, Module Federation, shadcn/ui, Radix UI primitives, and Tailwind CSS.
                </p>
              </TabsContent>
            </Tabs>
          </div>

          <div className="space-y-4 rounded-lg border p-4">
            <h3 className="text-sm font-medium uppercase tracking-wide text-muted-foreground">
              Quick stats
            </h3>
            <Separator />
            <div className="grid gap-3 text-sm">
              <div className="flex justify-between">
                <span>Services deployed</span>
                <span className="font-semibold">12</span>
              </div>
              <div className="flex justify-between">
                <span>Average build time</span>
                <span className="font-semibold">4m 20s</span>
              </div>
              <div className="flex justify-between">
                <span>Weekly releases</span>
                <span className="font-semibold">3</span>
              </div>
            </div>
            <Button className="w-full" variant="default">
              View architecture docs
            </Button>
          </div>
        </CardContent>
      </Card>

      <Accordion type="single" collapsible className="w-full">
        <AccordionItem value="vision">
          <AccordionTrigger>What drives the Remote team?</AccordionTrigger>
          <AccordionContent>
            We believe in giving product squads autonomy with guardrails.
            Our remote shell provides curated UI paradigms and resilient contracts for rapid iteration.
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="collaboration">
          <AccordionTrigger>How do we collaborate?</AccordionTrigger>
          <AccordionContent>
            Loosely coupled services, strongly aligned goals. We use design tokens, shared accessibility testing, and
            consistent tooling to ensure a cohesive experience.
          </AccordionContent>
        </AccordionItem>
        <AccordionItem value="contribute">
          <AccordionTrigger>How can you contribute?</AccordionTrigger>
          <AccordionContent>
            Start with our starter kit, explore the component library, and open a PR. We ship fast, review kindly,
            and document thoroughly.
          </AccordionContent>
        </AccordionItem>
      </Accordion>
    </div>
  )
}

export default About