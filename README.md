# py-inventory-v2-a2a
py-inventory-v2-a2a

```
# skills
check_inventory()             → deterministic
calculate_stock_coverage()    → deterministic
calculate_slope()              → Stats A2A
assess_stockout_risk()         → rules/model
decide_replenishment()         → agent + policy
request_replenishment()        → deterministic action

Inventory Skills
│
├── Observation
│   ├── check_inventory
│   ├── get_product_status
│   └── get_pending_orders
│
├── Analysis
│   ├── analyze_inventory_level
│   ├── calculate_stock_coverage
│   ├── analyze_sales_velocity
│   └── assess_stockout_risk
│
├── Decision
│   ├── evaluate_replenishment
│   ├── evaluate_halt
│   └── recommend_action
│
└── Action
    ├── request_replenishment
    ├── halt_product
    └── verify_action
```


```
| Component           | Responsibility                                 |
| ------------------- | ---------------------------------------------- |
| **A2A**             | Communication between agents                   |
| **Orchestrator**    | Coordinate agents/capabilities                 |
| **Reasoning**       | Interpret evidence and determine what it means |
| **Decision Engine** | Apply decision criteria/policies               |
| **State**           | Remember workflow progress                     |
| **Action Executor** | Perform side effects                           |
| **Domain**          | Business rules and models                      |
```