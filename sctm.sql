CREATE TABLE sctm_data (
    student TEXT,
    lesson TEXT,
    confidence REAL,
    data JSONB
);

INSERT INTO sctm_data(student, lesson, confidence, data)
VALUES('Alice', 'Physics', 0.92, '{"tip":"Visualize planets"}');
