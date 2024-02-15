using JuMP, GLPK

function maximize_plane_value(people_values, people_weights, friendship_values, plane_capacities)
    num_people = length(people_values)
    num_planes = length(plane_capacities)
    
    model = Model()
    set_optimizer(model, GLPK.Optimizer)

    @variable(model, x[1:num_people, 1:num_planes], Bin) # Variável para indicar a alocação de pessoas em aviões
    @variable(model, z[1:num_people, 1:num_people, 1:num_planes], Bin) # Variável para indicar se duas pessoas estão no mesmo avião    
    # Cada pessoa é atribuída a exatamente um avião
    for i in 1:num_people
        @constraint(model, sum(x[i, j] for j in 1:num_planes) == 1)
    end 
    
    # Restrição de capacidade para cada avião
    for j in 1:num_planes
        @constraint(model, sum(x[i, j] * people_weights[i] for i in 1:num_people) <= plane_capacities[j])
    end
    
    # Restrição para garantir que a variável z[i, k, j] seja 1 se e somente se x[i, j] e x[k, j] forem ambos 1
    for i in 1:num_people
        for k in 1:num_people
            for j in 1:num_planes
                @constraint(model, z[i, k, j] >= (x[i, j] + x[k, j]) - 1)
            end
        end
    end


     # Função objetivo: maximizar o valor total dos aviões considerando as relações de amizade
     @objective(model, Max, sum(x[i, j] * people_values[i] for i in 1:num_people, j in 1:num_planes) +
     sum(z[i, k, j] * friendship_values[i, k] for i in 1:num_people, k in 1:num_people, j in 1:num_planes if i != k))

    
    # Função objetivo: maximizar o valor total dos aviões considerando as relações de amizade
    #@objective(model, Max, (sum(x[i, j] * people_values[i] for i = 1:num_people, j = 1:num_planes)) + calcula_valor_amizade(y,friendship_values,num_people,num_planes) )
    #@objective(model, Max, sum(x[i, j] * people_values[i] for i = 1:num_people, j = 1:num_planes)) + total_friendship_value
    optimize!(model)
    
    println("Status da otimização: ", termination_status(model))

    if termination_status(model) == MOI.OPTIMAL
        println("Valor ótimo (soma de preferências): ", objective_value(model))

    else
        println("No optimal solution found.")
        return nothing
    end
end

function calcula_valor_amizade(y, fv,num_people,num_planes)
    aux= zeros(Int8, 60,60)
    aux = fv
    print(fv)
    y = complete_columns_with_zeros_3d(y,num_people,num_planes)
    Int64.(y)
        
    for i in 1:num_people
        for k in 1:num_people
            for j in 1:num_planes
                if y[i,k.j] == 1
                    total_fv = fv + (y[i,k,j] * fv[i,k])
                    print(total_fv)
                end
            end
        end
    end
    return total_fv
end

function le_instancia(nome_arquivo::AbstractString)
    linhas = readlines(nome_arquivo)
    
    numero_pessoas = parse(Int, linhas[1])
    valores_pessoas = parse.(Int, split(linhas[2]))
    relacoes_amizade = []
    for linha in linhas[3:numero_pessoas+2]
        numbers = parse.(Int, split(linha))
        push!(relacoes_amizade, numbers)
        
    end
    pesos_pessoas = parse.(Int, split(linhas[5 + numero_pessoas]))

    return numero_pessoas, valores_pessoas, relacoes_amizade, pesos_pessoas
end

function le_instancia(nome_arquivo::AbstractString)
    #     linhas = readlines(nome_arquivo)
        
    #     numero_pessoas = parse(Int, linhas[1])
    #     valores_pessoas = parse.(Int, split(linhas[2]))
    #     relacoes_amizade = []
    #     numbers = zeros(Int64,60,60)
    #     for linha in linhas[3:numero_pessoas+2]
    #         for col in 1:length(linha)
    #             numbers[linha][col] = parse.(Int, split(linha))
    #             push!(relacoes_amizade, numbers)
    #         end
    #     end
    #     pesos_pessoas = parse.(Int, split(linhas[5 + numero_pessoas]))
    
    #     return numero_pessoas, valores_pessoas, relacoes_amizade, pesos_pessoas
    # end
    

function calcula_capacidade_aviao(n_avioes::Int, pesos_pessoas::Vector{Int})
    capacidade_total = sum(pesos_pessoas)
    capacidade_por_aviao = Int(round(0.8 / n_avioes * capacidade_total))
    return capacidade_por_aviao
end

function complete_columns_with_zeros(matrix, n)
    completed_matrix = zeros(Int, n, n)

    for i in 1:n
        for j in n:-1:1
            if j > i
                completed_matrix[i, j] = matrix[i][j - i]
                # Atribuir elementos de matrix aos elementos correspondentes na diagonal inferior
                completed_matrix[j, i] = matrix[i][j - i]      
            end   
        end
    end
    return completed_matrix
end

function complete_columns_with_zeros_3d(matrix, n, np)
    completed_matrix = zeros(Int, n, n,j)

    for i in 1:n
        for k in 1:n
            for j in 1:n
                    completed_matrix[i,k,j] = matrix[i][k][j]
            end          
        end
    end
    return completed_matrix
end

n_pessoas, valores_pessoas, relacoes_amizade, pesos_pessoas = le_instancia("instances/vf01.dat")
m = 10
capacidade_por_aviao = calcula_capacidade_aviao(m, pesos_pessoas)

avioes = fill(200, m)

matrix_completa = complete_columns_with_zeros(relacoes_amizade, n_pessoas)

println(matrix_completa)

maximize_plane_value(valores_pessoas, pesos_pessoas, matrix_completa, avioes)