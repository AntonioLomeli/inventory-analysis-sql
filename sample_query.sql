-- This query generates a daily inventory reconciliation by aggregating operational movements 
-- and comparing them with physical inventory snapshots to detect discrepancies


SELECT  
mov.Fecha, mov.ID_Sucursal, mov.ID_Producto, prod.Nombre, 
sum(mov.Cantidad) filter (WHERE mov.ID_Salida IS NOT NULL) As Salidas_Totales,
sum(mov.Cantidad) filter (WHERE mov.ID_Traspaso IS NOT NULL) As Traspasos_Totales,
sum(mov.Cantidad) filter (WHERE mov.ID_Produccion IS NOT NULL) As Produccion_Total,

(Case WHEN inv.Fecha = '2023-07-01' then inv.Cantidad 
       else (SELECT Sum(Cantidad) FROM Inv_Fisico WHERE Fecha = '2023-07-01' AND ID_Producto = inv.ID_Producto AND ID_Sucursal = 1) end) As Inventario_Inicial,
(Case WHEN inv.Fecha = '2023-07-02' then inv.Cantidad end) As Inventario_Final


FROM Movimientos mov
INNER JOIN Inv_Fisico inv ON inv.ID_Producto = mov.ID_Producto
INNER JOIN Productos prod ON mov.ID_Producto = prod.ID_Producto

WHERE mov.Fecha = '2023-07-01' AND (inv.Fecha = '2023-07-01' OR inv.Fecha = '2023-07-02') AND mov.ID_Sucursal = 1  AND inv.Fecha != '2023-07-01' 
GROUP BY mov.ID_Producto, inv.Fecha
