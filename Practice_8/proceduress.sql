-- 2. Жаңа қолданушы қосу немесе бар болса нөмірін жаңарту процедурасы (Upsert)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM contacts WHERE username = p_name) THEN
        UPDATE contacts SET phone_number = p_phone WHERE username = p_name;
    ELSE
        INSERT INTO contacts(username, phone_number) VALUES(p_name, p_phone);
    END IF;
END;
$$;

-- 3. Көптеген қолданушыларды циклмен жаппай қосу және телефонды тексеру
CREATE OR REPLACE PROCEDURE insert_bulk_contacts(p_names VARCHAR[], p_phones VARCHAR[])
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
    v_phone TEXT;
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        v_phone := trim(p_phones[i]);
        
        -- Телефон нөмірі тек цифрлардан тұруын тексеру (мысалы, қарапайым валидация)
        IF v_phone ~ '^[0-9]+$' THEN
            IF EXISTS (SELECT 1 FROM contacts WHERE username = p_names[i]) THEN
                UPDATE contacts SET phone_number = v_phone WHERE username = p_names[i];
            ELSE
                INSERT INTO contacts(username, phone_number) VALUES(p_names[i], v_phone);
            END IF;
        ELSE
            RAISE NOTICE 'Invalid phone number format for user %: %', p_names[i], v_phone;
        END IF;
    END LOOP;
END;
$$;

-- 5. Аты немесе телефоны бойынша өшіру процедурасы
CREATE OR REPLACE PROCEDURE delete_contact_proc(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM contacts 
    WHERE username = p_value OR phone_number = p_value;
END;
$$;