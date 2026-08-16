-- Seed San Antonio locations and meals
-- Run after schema.sql

INSERT INTO locations (name, chain, type, address, lat, lng) VALUES
  ('Chipotle - Alamo Heights', 'Chipotle', 'restaurant', '4210 Broadway St, San Antonio, TX 78209', 29.4678, -98.4634),
  ('Chipotle - Downtown', 'Chipotle', 'restaurant', '733 E Houston St, San Antonio, TX 78205', 29.4267, -98.4847),
  ('Whataburger - St Mary''s', 'Whataburger', 'restaurant', '2427 N St Mary''s St, San Antonio, TX 78212', 29.4465, -98.4821),
  ('Panda Express - UTSA Loop', 'Panda Express', 'restaurant', '5706 UTSA Blvd, San Antonio, TX 78249', 29.5831, -98.6198),
  ('Torchy''s Tacos - The Pearl', 'Torchy''s Tacos', 'restaurant', '302 Pearl Pkwy, San Antonio, TX 78215', 29.4421, -98.4803),
  ('H-E-B - Alamo Heights', 'H-E-B', 'grocery', '300 W Olmos Dr, San Antonio, TX 78212', 29.4712, -98.4891),
  ('H-E-B - Southside', 'H-E-B', 'grocery', '4100 S New Braunfels Ave, San Antonio, TX 78223', 29.3856, -98.4612),
  ('H-E-B Plus - Bulverde', 'H-E-B', 'grocery', '2070 N Loop 1604 E, San Antonio, TX 78232', 29.6123, -98.4567);

INSERT INTO meals (location_chain, type, title, order_description, items, recipe, prep_minutes, base_price, per_serving_price, calories, protein_g, carbs_g, fat_g, goals) VALUES
  ('Chipotle', 'restaurant', 'High-Protein Bowl', 'Chicken bowl — white rice, pinto beans, fajita veggies, salsa, NO cheese/sour cream', '[]', '', 0, 9.25, NULL, 520, 42, 58, 12, ARRAY['gain_muscle','maintain']::health_goal[]),
  ('Chipotle', 'restaurant', 'Salad Cut', 'Chicken salad — lettuce, black beans, fajita veggies, salsa, NO rice', '[]', '', 0, 9.25, NULL, 340, 38, 22, 10, ARRAY['lose_weight','maintain']::health_goal[]),
  ('Whataburger', 'restaurant', 'Grilled Chicken', 'Grilled chicken sandwich — no mayo, add extra lettuce & tomato', '[]', '', 0, 6.49, NULL, 380, 32, 38, 9, ARRAY['gain_muscle','maintain','lose_weight']::health_goal[]),
  ('Whataburger', 'restaurant', 'Budget Burger', 'Whataburger Jr. — plain, no cheese, no mayo', '[]', '', 0, 4.29, NULL, 310, 16, 28, 14, ARRAY['lose_weight','maintain']::health_goal[]),
  ('Panda Express', 'restaurant', 'Protein Greens', 'Bowl — grilled teriyaki chicken + super greens (no rice)', '[]', '', 0, 8.99, NULL, 360, 36, 18, 14, ARRAY['lose_weight','gain_muscle']::health_goal[]),
  ('Panda Express', 'restaurant', 'Bulk Plate', 'Plate — black pepper chicken + chow mein (half portion rice)', '[]', '', 0, 9.49, NULL, 680, 34, 72, 22, ARRAY['gain_muscle']::health_goal[]),
  ('Torchy''s Tacos', 'restaurant', 'Street Taco Boost', 'Mr. Orange — corn tortilla, add grilled chicken, no queso', '[]', '', 0, 5.50, NULL, 420, 28, 32, 18, ARRAY['gain_muscle','maintain']::health_goal[]),
  ('H-E-B', 'grocery', 'Muscle Bowl', '1 dozen eggs + spinach + black beans', '["H-E-B dozen large eggs ($2.89)", "Fresh spinach 10oz ($2.49)", "H-E-B black beans 15oz ($0.89)"]', 'Scramble 3 eggs with spinach. Heat black beans. Makes 4 servings — ~$1.57/meal, 5 min.', 5, 6.27, 1.57, 380, 28, 22, 18, ARRAY['gain_muscle','maintain']::health_goal[]),
  ('H-E-B', 'grocery', 'Rotisserie Wraps', 'Rotisserie chicken + tortillas + salsa', '["H-E-B rotisserie chicken ($7.98)", "Whole wheat tortillas 8ct ($2.29)", "H-E-B salsa 16oz ($1.99)"]', 'Shred chicken, wrap with salsa. Makes 4 wraps — ~$3.07/wrap, 3 min each.', 3, 12.26, 3.07, 320, 32, 28, 8, ARRAY['gain_muscle','maintain']::health_goal[]),
  ('H-E-B', 'grocery', 'Budget Cut Bowl', 'Canned tuna + microwave rice + frozen broccoli', '["Chicken of the Sea tuna 5oz x2 ($1.98)", "H-E-B microwavable rice ($1.49)", "Frozen broccoli 12oz ($1.29)"]', 'Microwave rice & broccoli, mix with tuna. Makes 2 bowls — ~$2.38/bowl, 5 min.', 5, 4.76, 2.38, 410, 32, 48, 6, ARRAY['gain_muscle','lose_weight','maintain']::health_goal[]),
  ('H-E-B', 'grocery', 'Light & Lean', 'Greek yogurt + banana + peanut butter', '["H-E-B plain Greek yogurt 32oz ($3.99)", "Banana bunch ($0.69)", "H-E-B natural PB 16oz ($2.99)"]', '1 cup yogurt + 1 banana + 1 tbsp PB. Makes 4 servings — ~$1.92/meal, 2 min.', 2, 7.67, 1.92, 340, 22, 38, 12, ARRAY['lose_weight','maintain']::health_goal[]);
