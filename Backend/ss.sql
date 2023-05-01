SELECT
    m.id AS msgid,
    m.time AS time,
    usen.name AS sendername,
    usen.email AS senderemail,
    urec.name AS receivername,
    urec.email AS receiveremail,
    m.subject AS subject,
    m.message AS message,
    s.label AS label
FROM
    starred s
    JOIN messages m ON s.messageid = m.id
    JOIN users usen ON m.sender = usen.id
    JOIN users urec ON m.receiver = urec.id
WHERE starredby=%s ORDER BY id DESC;

SELECT m.id AS msgid, m.time AS time, usen.name AS sendername, usen.email AS senderemail,
    urec.name AS receivername, urec.email AS receiveremail, m.subject AS subject,
    m.message AS message, s.label AS label
FROM starred s
    JOIN messages m ON s.messageid = m.id
    JOIN users usen ON m.sender = usen.id
    JOIN users urec ON m.receiver = urec.id
WHERE starredby=1 ORDER BY s.id DESC;

query = """SELECT m.id, m.time, usen.name AS sendername, usen.email AS senderid, urec.name AS receivername, urec.email as receiverid, m.isstarbyrecv, m.subject,m.message FROM messages m 
JOIN users usen ON m.sender = usen.id
JOIN users urec ON m.receiver = urec.id
WHERE m.receiver = %s AND isdelbyrecv = false ORDER BY id DESC"""
