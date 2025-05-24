#  FastAPI CRUD – Project TODOs

##  Core Features
- [x] Add pagination to `/bats/` list endpoint
- [x] Add search filter by price and order
- [x] Write unit tests for `create_bat` and `get_bats`
- [x] Protect all routes with `get_current_user`

##  Testing
- [ ] Add tests for search & pagination
- [ ] Add invalid input test cases (e.g., bad brand)

##  Auth
- [x] Implement JWT login/register
- [x] Create a role-based access example (admin vs user)

##  Refactor Ideas
- [x] Clean up `crud.py` with base service layer
- [ ] Move shared logic to `utils/`

##  Notes
- [ ] Consider renaming endpoints from `/bats/` to `/items/` if reused later
- [ ] Think about how this scales to multiple models
