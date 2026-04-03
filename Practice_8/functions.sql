-- 1. Үлгі бойынша іздеу функциясы (Аты немесе телефоны бойынша)
CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p_pattern TEXT)
RETURNS TABLE(id INT, username VARCHAR, phone_number VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.id, c.username, c.phone_number 
    FROM contacts c
    WHERE c.username ILIKE '%' || p_pattern || '%'
       OR c.phone_number LIKE '%' || p_pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- 4. Пагинация арқылы деректерді шығару функциясы
CREATE OR REPLACE FUNCTION get_contacts_paginated(p_limit INT, p_offset INT)
RETURNS TABLE(id INT, username VARCHAR, phone_number VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT c.id, c.username, c.phone_number 
    FROM contacts c
    ORDER BY c.id
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;