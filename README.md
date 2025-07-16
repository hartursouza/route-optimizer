# Sistema de Otimização de Rotas

![Badge](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)

Projeto desenvolvido como parte da disciplina **Programação Avançada** da **UFRN - Departamento de Engenharia de Comunicações**, com o objetivo de criar um sistema web que auxilie usuários na geração de rotas otimizadas com foco em economia, eficiência e facilidade de uso.

---

## 📌 Resumo

Este sistema web permite traçar rotas otimizadas entre múltiplos endereços, exibindo no mapa o trajeto mais eficiente, além de informações como:

- Distância total
- Tempo estimado de viagem
- Custos associados (ex: combustível e taxas urbanas)

### Público-Alvo
- Transportadoras
- Motoristas e entregadores autônomos
- Empresas logísticas

---

## 🚀 Funcionalidades

- ✅ Geração de rotas otimizadas via OpenRouteService
- ✅ Visualização de rotas no mapa com Leaflet.js
- ✅ Cálculo de distância e duração da viagem
- ✅ Salvamento de rotas no banco de dados
- ✅ Visualização e exclusão de rotas cadastradas
- 🚧 Estimativa de custo com base em consumo e taxas (em desenvolvimento)
- 🚧 Cadastro e login de usuários (próxima etapa)

---

## 💡 Estórias de Usuário

| ID  | Estória | Prioridade |
|-----|--------|------------|
| EU1 | Como entregador autônomo, quero gerar rotas otimizadas para garantir que as entregas sejam realizadas de forma planejada e eficiente. | Alta |
| EU2 | Como gestor de transporte, quero calcular o custo estimado de uma rota, considerando combustível, taxas urbanas e custos trabalhistas. | Alta |

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.12+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy + Flask-Migrate](https://flask-sqlalchemy.palletsprojects.com/)
- [PostgreSQL (Render)](https://render.com/)
- [OpenRouteService API](https://openrouteservice.org/)
- [Leaflet.js](https://leafletjs.com/)
- [HTML + Bootstrap 5](https://getbootstrap.com/)

---

## 📦 Instalação

### 1. Clone o projeto

```bash
git clone https://github.com/hartursouza/route-optimizer.git
cd route-optimizer
