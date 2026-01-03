dmf-music-platform/
├── infrastructure/
│   ├── terraform/
│   │   ├── main.tf               # VPC-less serverless infra
│   │   ├── api-gateway.tf        # API Gateway routes
│   │   ├── lambda.tf             # All Lambda functions
│   │   ├── dynamodb.tf           # Bot tables, roster tables
│   │   ├── iam.tf                # Least privilege + Da’Riyah role
│   │   ├── kms.tf                # Encryption keys for brain + bots
│   │   └── outputs.tf
│   └── scripts/
│       ├── deploy.sh
│       ├── destroy.sh
│       └── rotate-keys.sh
│
├── backend/
│   ├── api-wall/                 # API-key firewall
│   │   ├── verifyKey.ts
│   │   ├── keyRouter.ts
│   │   └── daryiah-access.ts
│   ├── lambdas/
│   │   ├── daryiah-core/         # Da’Riyah’s brain Lambda
│   │   │   ├── index.ts
│   │   │   ├── memory.json
│   │   │   ├── skills/
│   │   │   └── router.ts
│   │   ├── bots/
│   │   │   ├── orchestrator.ts   # commands 500 bots
│   │   │   ├── generate.ts       # bot generator
│   │   │   └── workers/
│   │   │       ├── Bot001/
│   │   │       ├── Bot002/
│   │   │       └── ... up to Bot500/
│   │   ├── roster/
│   │   │   ├── addArtist.ts
│   │   │   ├── syncCatalog.ts
│   │   │   └── analytics.ts
│   │   ├── distro/
│   │   │   ├── submitRelease.ts
│   │   │   └── trackStatus.ts
│   │   └── system/
│   │       ├── health.ts
│   │       ├── metrics.ts
│   │       └── auditLogs.ts
│   ├── ai-router/
│   │   ├── openai.ts
│   │   ├── googleai.ts
│   │   └── daryiah-model-router.ts
│   └── shared/
│       ├── mongo.ts              # MongoDB Data API client
│       ├── supabase.ts
│       ├── responses.ts
│       └── types.ts
│
├── frontend/
│   ├── next.config.mjs
│   ├── package.json
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx              # DMF dashboard home
│   │   ├── bots/
│   │   │   └── page.tsx
│   │   ├── roster/
│   │   │   └── page.tsx
│   │   ├── releases/
│   │   │   └── page.tsx
│   │   ├── distro/
│   │   │   └── page.tsx
│   │   └── settings/
│   │       └── page.tsx
│   ├── components/
│   └── styles/
│
├── dariyah/                       # The Brain
│   ├── personality.json
│   ├── memory-core.json
│   ├── intent-router.ts
│   ├── scoring-system.ts
│   ├── chain-of-thought.ts
│   ├── task-delegator.ts
│   └── bot-assignments.ts
│
├── bots/                          # 500 workers
│   ├── bot.config.global.json
│   ├── templates/
│   │   ├── personality.template.json
│   │   └── skills.template.json
│   ├── Bot001/
│   ├── Bot002/
│   └── ... up to Bot500/
│
├── docs/
│   ├── architecture.md
│   ├── dariyah.md
│   ├── bot-network.md
│   ├── api-wall.md
│   ├── distro-pipeline.md
│   └── security.md
└── scripts/
    ├── generate-bot.ts
    ├── sync-roster.ts
    └── publish-release.ts
