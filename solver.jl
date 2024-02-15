using JuMP, GLPK

function maximize_plane_value(people_values, people_weights, friendship_values, plane_capacities)
    num_people = length(people_values)
    num_planes = length(plane_capacities)
    
    model = Model()
    set_optimizer(model, GLPK.Optimizer)

    @variable(model, x[1:num_people, 1:num_planes], Bin) # Variável para indicar a alocação de pessoas em aviões
    @variable(model, y[1:num_people, 1:num_people, 1:num_planes], Bin)  # Variável auxiliar para indicar se duas pessoas estão no mesmo avião
    
    # Cada pessoa é atribuída a exatamente um avião
    for i in 1:num_people
        @constraint(model, sum(x[i, j] for j in 1:num_planes) == 1)
    end
    
    # Restrição de capacidade para cada avião
    for j in 1:num_planes
        @constraint(model, sum(x[i, j] * people_weights[i] for i in 1:num_people) <= plane_capacities[j])
    end
    
    # Se duas pessoas estão juntas em um avião, a variável auxiliar correspondente é 1
    #= 
    for i in 1:num_people
        for k in 1:num_people
            for j in 1:num_planes
                @constraint(model, y[i, k, j] >= x[i, j] + x[k, j] - 1)
            end
        end
    end 
    =#
    
    # Se duas pessoas estão juntas em um avião, o valor da relação entre elas é adicionado ao valor total
    @expression(model, total_friendship_value, sum(y[i, k, j] * friendship_values[i, k] for i in 1:num_people for k in 1:num_people-i for j in 1:num_planes))

    # Função objetivo: maximizar o valor total dos aviões considerando as relações de amizade
    @objective(model, Max, sum(x[i, j] * people_values[i] for i = 1:num_people, j = 1:num_planes)) + total_friendship_value 

    optimize!(model)
    
    println("Status da otimização: ", termination_status(model))

    if termination_status(model) == MOI.OPTIMAL
        println("Valor ótimo (soma de preferências): ", objective_value(m))

    else
        println("No optimal solution found.")
        return nothing
    end
end

function le_instancia(nome_arquivo::AbstractString)
    linhas = readlines(nome_arquivo)
    
    numero_pessoas = parse(Int, linhas[1])
    valores_pessoas = parse.(Int, split(linhas[2]))
    relacoes_amizade = [parse.(Int, split(linha)) for linha in linhas[3:numero_pessoas+2]]
    pesos_pessoas = parse.(Int, split(linhas[5 + numero_pessoas]))

    return numero_pessoas, valores_pessoas, relacoes_amizade, pesos_pessoas
end

function calcula_capacidade_aviao(n_avioes::Int, pesos_pessoas::Vector{Int})
    capacidade_total = sum(pesos_pessoas)
    capacidade_por_aviao = Int(round(0.8 / n_avioes * capacidade_total))
    return capacidade_por_aviao
end

n_pessoas, valores_pessoas, relacoes_amizade, pesos_pessoas = le_instancia("instances/vf01.dat")
m = 10
capacidade_por_aviao = calcula_capacidade_aviao(m, pesos_pessoas)
avioes = fill(capacidade_por_aviao, m)

maximize_plane_value(valores_pessoas, pesos_pessoas, relacoes_amizade, avioes)