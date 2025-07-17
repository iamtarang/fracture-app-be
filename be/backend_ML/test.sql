DECLARE
    v_employee_name VARCHAR2(100);
    v_salary NUMBER;
BEGIN
    -- Take input employee name from user
    v_employee_name := '&Enter_Employee_Name';
    
    -- Fetch employee salary
    SELECT SAL INTO v_salary FROM EMPLOYEES WHERE EMP_NAME = v_employee_name;
    
    -- Check if the employee is a manager or analyst
    IF (SELECT COUNT(*) FROM EMPLOYEES WHERE EMP_NAME = v_employee_name AND (JOB = 'MANAGER' OR JOB = 'ANALYST')) > 0 THEN
        -- Give a raise of 15%
        v_salary := v_salary * 1.15;
        DBMS_OUTPUT.PUT_LINE('Employee ' || v_employee_name || ' is either a manager or analyst. Salary increased by 15%.');
    ELSE
        -- Decrease salary by 12%
        v_salary := v_salary * 0.88;
        DBMS_OUTPUT.PUT_LINE('Employee ' || v_employee_name || ' is not a manager or analyst. Salary decreased by 12%.');
    END IF;
    
    -- Update the salary
    UPDATE EMPLOYEES SET SAL = v_salary WHERE EMP_NAME = v_employee_name;
    
    COMMIT;
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('Employee ' || v_employee_name || ' not found.');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('An error occurred.');
END;
/


DECLARE
    v_department_number NUMBER;
    v_max_salary NUMBER;
    v_total_employees NUMBER;
BEGIN
    -- Take input department number from user
    v_department_number := &Enter_Department_Number;
    
    -- Fetch maximum salary and total number of employees in the department
    SELECT MAX(SAL), COUNT(*)
    INTO v_max_salary, v_total_employees
    FROM EMPLOYEES
    WHERE DEPARTMENT_NUMBER = v_department_number;
    
    DBMS_OUTPUT.PUT_LINE('Maximum salary in department ' || v_department_number || ': ' || v_max_salary);
    DBMS_OUTPUT.PUT_LINE('Total number of employees in department ' || v_department_number || ': ' || v_total_employees);
EXCEPTION
    WHEN NO_DATA_FOUND THEN
        DBMS_OUTPUT.PUT_LINE('Department ' || v_department_number || ' not found.');
    WHEN OTHERS THEN
        DBMS_OUTPUT.PUT_LINE('An error occurred.');
END;
/
